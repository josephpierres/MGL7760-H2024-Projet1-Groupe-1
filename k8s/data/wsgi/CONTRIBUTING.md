# pour executer local:

# creation d'un image mysql `a partir du repertoire mysql

cd mysql && docker build -t mysql_db .

# lancer le conteneur 
docker run --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=password -d mysql_db:latest

# echo "Stopping mysql container..."
docker stop mysql

# echo "Removing mysql container..."
docker rm mysql