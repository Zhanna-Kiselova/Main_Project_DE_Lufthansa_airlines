#!/bin/bash
# 1) Path to the main project folder 
cd C:\Users\Zhanna\Desktop\Main_Project_DE_Lufthansa_airlines\ 

# 2) Loading the mongo image
docker image pull mongo:latest

# 3) Image deployment as container 
docker run -d -p 27017-27019:27017-27019 --name container_mongodb mongo

# 4) Connection to MongoDB. 
docker start container_mongodb

# 5) We launch the application with one commande 
docker-compose up 