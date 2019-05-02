if [ $# -eq 0 ]; then
	htype='intent'
	
    docker run -d --name=rabbitmq -p 5672:5672 -e RABBITMQ_DEFAULT_USER='admin'  -e RABBITMQ_DEFAULT_PASS='mypass' rabbitmq:alpine
    docker run -d --name=postgis -p 5432:5432 -e POSTGRES_PASSWORD='postgres'  mdillon/postgis	
else
	htype='arm.intent'
	
	docker run -d --name=rabbitmq -p 5672:5672 -e RABBITMQ_DEFAULT_USER='admin'  -e RABBITMQ_DEFAULT_PASS='mypass' rabbitmq:alpine
    docker run -d --name=postgis -p 5432:5432 -e POSTGRES_PASSWORD='postgres'  tobi312/rpi-postgresql-postgis
fi

docker run -d --name=discovery -v `pwd`/config.json:/config.json -p 443:443  fogflow/discovery:$htype

docker run -d --name=designer -v `pwd`/config.json:/app/config.json -p 1030:1030 -p 80:80  fogflow/designer:$htype

docker run -d --name=broker -v `pwd`/config.json:/config.json -p 8080:8080  fogflow/broker:$htype

docker run -d --name=master -v `pwd`/config.json:/config.json -p 1060:1060  fogflow/master:$htype

docker run -d --name=worker -v `pwd`/config.json:/config.json -v /tmp:/tmp -v /var/run/docker.sock:/var/run/docker.sock fogflow/worker:$htype

