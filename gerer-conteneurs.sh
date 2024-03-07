#!/bin/bash

# Fonction pour afficher l'utilisation correcte
usage() {
    echo "Utilisation : $0 [install|create|import|start|stop|destroy]"
    exit 1
}

# Vérifier si une option est spécifiée
if [ -z "$1" ]; then
    usage
fi

# Nom du conteneur MySQL
MYSQL_CONTAINER="mysql"

# Nom des conteneurs d'application 
WSGI_CONTAINER="wsgi0 wsgi1 wsgi2"


# Nom du conteneur du serveur web
NGINX_CONTAINER="nginx"

# Nom du conteneur Redis
REDIS_CONTAINER="redis"

# Nom du réseau Docker
DOCKER_NETWORK="front_network back_network"

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
    docker compose build
}

# Importation de nouveaux livres
import_books() {
  PYTHONSCRIPT="$(pwd)/import_books.py"  
  echo "Vérifions l'état du conteneur mysql"
  if docker inspect -f '{{.State.Running}}' mysql > /dev/null 2>&1; then
    python3 $PYTHONSCRIPT 
  else
    echo "Aucun conteneur mysql en cours d'exécution"
    echo "\n il faut que le conteneur mysql soit demarres pour executer cette tache"
    
  fi
}

# Fonction pour démarrer les conteneurs
start_containers() {
    docker compose up -d
}

# Fonction pour arrêter les conteneurs
stop_containers() {
    docker compose stop
}

# Fonction pour détruire l'environnement de développement
destroy_environment() {
    # Stopper et supprimer tous les conteneurs
    docker compose down

    # Supprimer les réseaux et les conteneurs Docker 
    docker network rm -f $DOCKER_NETWORK    
    docker kill $NGINX_CONTAINER 
    docker kill $WSGI_CONTAINER 
    docker kill $REDIS_CONTAINER
    docker kill $MYSQL_CONTAINER
    # supression des images
    docker rmi -f "$NGINX_CONTAINER":1.25.3 
    docker rmi -f wsgi0:1.0  wsgi1:1.0 wsgi2:1.0
    docker rmi -f "$REDIS_CONTAINER":7.2.4  
    docker rmi -f "$MYSQL_CONTAINER":8.0.22  
    # supression des volumes       
    docker volume rm -f mysql_volume
    docker system prune -f
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
