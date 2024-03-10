#!/bin/bash
# MySQL configuration
MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"
MYSQL_DATABASE = "gestion_bibliotheque"
MYSQL_USER = "root"
MYSQL_PASSWORD = "password"

# Path to the CSV file
CSV_FILE = "biblio.csv"

echo "Cleaning up existing mysql container"

echo "Stopping mysql container..."
docker stop mysql

echo "Removing mysql container..."
docker rm mysql

echo " create the image"
docker build -t mysql_db ./mysql

echo " lunch the container" 
docker run --name mysql -dp 3306:3306 -e MYSQL_ROOT_PASSWORD=password -d mysql_db:latest

docker exec -i --name mysql  -v $PWD/mysql/data:/var/lib/mysql mysql -h{MYSQL_HOST} -P{MYSQL_PORT} -u{MYSQL_USER} -p{MYSQL_PASSWORD} {MYSQL_DATABASE}

echo "Started container, forwarded docker host port 3306 to container, connect using details: root:password"
echo "e.g. mysql -h127.0.0.1 -uroot -ppassword"
echo "where 192.168.59.103 is the IP of your docker host"