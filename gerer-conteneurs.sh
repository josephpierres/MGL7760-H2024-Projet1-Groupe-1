#!/bin/bash

# Fonction pour afficher l'utilisation correcte
usage() {
    echo "Utilisation : $0 [create|import|start|stop|destroy]"
    exit 1
}

# Vérifier si une option est spécifiée
if [ -z "$1" ]; then
    usage
fi

# Répertoire contenant le code source
SOURCE_DIR="/chemin/vers/votre/code/source"

# Répertoire contenant le fichier SQL initial et le fichier CSV
DATA_DIR="/chemin/vers/vos/donnees"

# Nom du conteneur MySQL
MYSQL_CONTAINER="nom_mysql"

# Nom du conteneur Redis
REDIS_CONTAINER="nom_redis"

# Nom du réseau Docker
DOCKER_NETWORK="nom_reseau"

# installer Docker et Docker Compose sur Ubuntu
install_docker(){
    # Mise à jour du système
    sudo apt-get update
    sudo apt-get upgrade -y

    # Installation des dépendances
    sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

    # Ajout de la clé GPG officielle de Docker
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

    # Configuration du référentiel stable de Docker
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    # Installation de Docker
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io

    # Ajout de l'utilisateur actuel au groupe docker (pour exécuter Docker sans sudo)
    sudo usermod -aG docker $USER

    # Installation de Docker Compose
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose

    # Afficher les versions installées
    echo "Docker version:"
    docker --version

    echo "Docker Compose version:"
    docker-compose --version

    # Redémarrer pour appliquer les changements (assurez-vous que votre session soit réouverte)
    echo "Redémarrez votre session pour appliquer les changements."
}

# Fonction pour créer l'environnement de développement
create_environment() {
    # Créer un réseau Docker
    docker network create $DOCKER_NETWORK

    # Démarrer le conteneur MySQL
    docker run -d --name $MYSQL_CONTAINER --network $DOCKER_NETWORK -e MYSQL_ROOT_PASSWORD=root -v $DATA_DIR/db.sql:/docker-entrypoint-initdb.d/db.sql mysql:latest

    # Démarrer le conteneur Redis
    docker run -d --name $REDIS_CONTAINER --network $DOCKER_NETWORK redis:latest

    # Build et démarrer les conteneurs Flask et Nginx
    cd $SOURCE_DIR
    docker-compose up --build -d
}

# Fonction pour importer de nouveaux livres depuis un fichier CSV
import_books() {
    # Stopper le conteneur Flask pour éviter les conflits lors de l'importation
    docker-compose stop flask

    # Importer les livres depuis le fichier CSV
    docker exec -it $MYSQL_CONTAINER mysql -uroot -proot -e "USE votre_base_de_donnees; LOAD DATA LOCAL INFILE '/chemin/vers/vos/donnees/livres.csv' INTO TABLE livre FIELDS TERMINATED BY ',' IGNORE 1 LINES;"

    # Redémarrer le conteneur Flask
    docker-compose start flask
}

# Importation de nouveaux livres
import_books() {
CSV_FILE="nouveaux_livres.csv"
docker exec -i python_flask_container python3 import_books.py "$CSV_FILE"
}

# Fonction pour démarrer les conteneurs
start_containers() {
    docker-compose start
}

# Fonction pour arrêter les conteneurs
stop_containers() {
    docker-compose stop
}

# Fonction pour détruire l'environnement de développement
destroy_environment() {
    # Stopper et supprimer tous les conteneurs
    docker-compose down

    # Supprimer le réseau Docker
    docker network rm $DOCKER_NETWORK
}

# Exécuter l'option spécifiée
case "$1" in
    install)
        install_docker
        ;;
    create)
        create_environment
        ;;
    import)
        import_books
        ;;
    start)
        start_containers
        ;;
    stop)
        stop_containers
        ;;
    destroy)
        destroy_environment
        ;;
    *)
        usage
        ;;
esac
