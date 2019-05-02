echo "-----stop all components-----"
docker stop broker 
docker stop worker 
docker stop master 
docker stop discovery 
docker stop designer 
docker stop rabbitmq 
docker stop postgis 

echo "-----remove all containers-----"
docker rm broker 
docker rm worker 
docker rm master 
docker rm discovery 
docker rm designer 
docker rm rabbitmq 
docker rm postgis 

