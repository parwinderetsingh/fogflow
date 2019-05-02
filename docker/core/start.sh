tag="intent"
cfile="config.json"

while getopts "f:t:" opt; do
    case $opt in
        f ) cfile="$OPTARG";;
        t ) tag="$OPTARG";;
        \?) echo "Invalid option: -"$OPTARG"" >&2
            exit 1;;
        : ) echo "Option -"$OPTARG" requires an argument." >&2
            exit 1;;
      esac
    done
echo "tag is "$tag""
echo "configuration file is "$cfile""

if [ "$tag" = "arm" ]; then
    echo "start rabbitmq"
    docker run -d --name=rabbitmq -p 5672:5672 -e RABBITMQ_DEFAULT_USER='admin'  -e RABBITMQ_DEFAULT_PASS='mypass' rabbitmq:alpine

    echo "start postgis"
    docker run -d --name=postgis -p 5432:5432 -e POSTGRES_PASSWORD='postgres'  tobi312/rpi-postgresql-postgis
else
    echo "start rabbitmq"
    docker run -d --name=rabbitmq -p 5672:5672 -e RABBITMQ_DEFAULT_USER='admin'  -e RABBITMQ_DEFAULT_PASS='mypass' rabbitmq:alpine

    echo "start postgis"
    docker run -d --name=postgis -p 5432:5432 -e POSTGRES_PASSWORD='postgres'  mdillon/postgis	
fi

echo "start discovery"
docker run -d --name=discovery -v `pwd`/$cfile:/config.json -p 443:443  fogflow/discovery:$tag

echo "start designer"
docker run -d --name=designer -v `pwd`/$cfile:/app/config.json -p 1030:1030 -p 80:80  fogflow/designer:$tag

echo "start broker"
docker run -d --name=broker -v `pwd`/$cfile:/config.json -p 8080:8080  fogflow/broker:$tag

echo "start master"
docker run -d --name=master -v `pwd`/$cfile:/config.json -p 1060:1060  fogflow/master:$tag

echo "start worker"
docker run -d --name=worker -v `pwd`/$cfile:/config.json -v /tmp:/tmp -v /var/run/docker.sock:/var/run/docker.sock fogflow/worker:$tag

