

printStep(){
    echo ""
    echo ""
    echo "[" $1 "STARTED]"
    sleep 1 
}
sudo service docker start
printStep "DEPLOYMENT"

printStep "DOWN PREVIOUS CONTAINERS"
sudo docker-compose down 

printStep "PRUNING DOCKER"
sudo docker system prune -f

printStep 'DOCKER_COMPOSE BUILD'
sudo docker-compose build

printStep 'DOCKER_COMPOSE UP'
sudo docker-compose up



