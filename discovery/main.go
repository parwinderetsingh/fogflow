package main

import (
	"flag"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"strconv"
	"syscall"

	"github.com/ant0ine/go-json-rest/rest"
	"github.com/mmcloughlin/geohash"

	. "github.com/smartfog/fogflow/common/config"
	. "github.com/smartfog/fogflow/common/ngsi"
)

func main() {
	cfgFile := flag.String("f", "config.json", "A configuration file")
	flag.Parse()
	config, err := LoadConfig(*cfgFile)
	if err != nil {
		os.Stderr.WriteString(fmt.Sprintf("%s\n", err.Error()))
		INFO.Println("please specify the configuration file, for example, \r\n\t./discovery -f config.json")
		os.Exit(-1)
	}

	config.Discovery.DBCfg.Host = config.InternalIP

	// load the routing table and announce itself
	rTable := Routing{}
	mySiteInfo := SiteInfo{}
	mySiteInfo.IsLocalSite = true
	mySiteInfo.ExternalAddress = fmt.Sprintf("%s:%d", config.ExternalIP, config.Discovery.Port)
	mySiteInfo.GeohashID = geohash.EncodeWithPrecision(config.PLocation.Latitude,
		config.PLocation.Longitude,
		config.Precision)
	rTable.Init(config.RootDiscovery, mySiteInfo)

	// initialize IoT Discovery
	iotDiscovery := FastDiscovery{routingTable: &rTable}
	iotDiscovery.Init(&config.Discovery.DBCfg)

	// start REST API server
	router, err := rest.MakeRouter(
		// standard ngsi9 API
		rest.Post("/ngsi9/registerContext", iotDiscovery.RegisterContext),
		rest.Post("/ngsi9/discoverContextAvailability", iotDiscovery.DiscoverContextAvailability),
		rest.Post("/ngsi9/subscribeContextAvailability", iotDiscovery.SubscribeContextAvailability),
		rest.Post("/ngsi9/unsubscribeContextAvailability", iotDiscovery.UnsubscribeContextAvailability),
		rest.Delete("/ngsi9/registration/#eid", iotDiscovery.deleteRegisteredEntity),

		// interaction across sites for distributed discovery
		rest.Post("/ngsi9/interSiteContextAvailabilityQuery", iotDiscovery.SiteDiscoverContextAvailability),
		rest.Post("/ngsi9/interSiteContextAvailabilitySubscribe", iotDiscovery.SiteSubscribeContextAvailability),
		rest.Post("/ngsi9/interSiteContextAvailabilityUnsubscribe", iotDiscovery.SiteUnsubscribeContextAvailability),

		// convenient ngsi9 API
		rest.Get("/ngsi9/registration/#eid", iotDiscovery.getRegisteredEntity),
		rest.Get("/ngsi9/subscription/#sid", iotDiscovery.getSubscription),
		rest.Get("/ngsi9/subscription", iotDiscovery.getSubscriptions),

		// maintain the routing tables for distributed discovery
		rest.Post("/ngsi9/broadcast", iotDiscovery.onBroadcast),
		rest.Get("/ngsi9/sitelist", iotDiscovery.getAllSites),
		rest.Post("/ngsi9/querysite", iotDiscovery.onQuerySiteByScope),

		// for health check
		rest.Get("/ngsi9/status", iotDiscovery.getStatus),

		// hearbeat from active brokers
		rest.Post("/ngsi9/broker", iotDiscovery.onBrokerHeartbeat),

		// proxy to forward the entity update from other site to the broker within the local site
		rest.Post("/proxy/updateContext", iotDiscovery.onForwardContextUpdate),
		rest.Get("/proxy/brokerlist", iotDiscovery.getBrokerList),
	)
	if err != nil {
		log.Fatal(err)
		os.Exit(-1)
	}

	api := rest.NewApi()
	api.Use(rest.DefaultCommonStack...)

	api.Use(&rest.CorsMiddleware{
		RejectNonCorsRequests: false,
		OriginValidator: func(origin string, request *rest.Request) bool {
			return true
		},
		AllowedMethods:                []string{"GET", "POST", "PUT"},
		AllowedHeaders:                []string{"Accept", "Content-Type", "X-Custom-Header", "Origin"},
		AccessControlAllowCredentials: true,
		AccessControlMaxAge:           3600,
	})

	api.SetApp(router)

	go func() {
		fmt.Printf("Starting IoT Discovery on port %d\n", config.Discovery.Port)
		panic(http.ListenAndServe(":"+strconv.Itoa(config.Discovery.Port), api.MakeHandler()))
	}()

	// wait for Control +C to quit
	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt)
	signal.Notify(c, syscall.SIGTERM)
	<-c

	fmt.Println("Stoping IoT Discovery")

	iotDiscovery.Stop()
}
