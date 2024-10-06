Notre environnement de travail est une machine Windows et pour les besoins du projet on doit respecter la pile technologique : 
OS: Ubuntu:22.04
Serveur Web: Nginx
Serveur App: Python/flask
Serveur BD: Mysql
Cache memoire: Redis
Architecture: SOA sur Docker
pour se faire nous avons téléchargé la version 7.0 de VirtualBox et installer comme hyperviseur sur Windows.
Virtualbox install, nous avons télechargé Ubuntu 22.04 et avec 8GB de memoire pour un environnement virtuel optimal pour le projet.

# VOILA LA STRUCTURE DES APPELS CLIENTS
HTTP client <-> Nginx <-> uWSGI <-> Python app <-> Mysql
le client http fait appel a une page sur son navigateur, Nginx communique une page statique stocker dans son conteneur ou une page dynamique creer par python.Pour faire communiquer Nginx et Python nous utilisons un WSGI le uwsgi comme un proxy  serveur
## Commencement des installations
avant d´installer l´environnement et nous assurer de le telecharger la bonne version des choses nous avons passer la commande suivant sur linux 
lsb_release -cs
qui affiche les informations necessaires sur l´architecture de la machine utilisée
ensuite nous avons besoins du privilège root dans notre profil pour avancer avec githles installations, la suite de commandes suivantes:
su root    // nous permet d´executer dans le terminal des commandes en tant que root
usermod -aG sudo $USER  // permet d´ajouter l´utilisateur user1 au groupe sudo -a: ajouter -G: au groupe
newgrp sudo   // rafraichir le groupe sudo pour rentre actif les nouveaux ajouts

## Installation de Visual Studio Code ##
Nous allons sur le site de Microsoft https://code.visualstudio.com/docs/?dv=linux64_deb et telecharger le fichier code_1.85.2-1705561292_amd64.deb dans le repertoire de travail /download et avec la commande:
cd Downloads
sudo apt install ./code_1.85.2-1705561292_amd64.deb
l´installation de Visual Studio Code est lancée à partir du terminal de linux.

Une fois vscode installé, nous installons les extentions 
Docker : cet extention rend facile l´execution, la gesstion et le deploiement des applications containarisé à partir de VSCode
GitHub Pull Request and Issues: This extension allows you to review and manage GitHub pull requests and issues in Visual Studio Code. 
Code Runner : nous permet d´executer du code python, htm, javascript etc.. à partir de l´IDE
Git Extention Pack
Pylance: Pylance is an extension that works alongside Python in Visual Studio Code to provide performant language support.
Python: A Visual Studio Code extension with rich support for the Python language (for all actively supported versions of the language: >=3.7), including features such as IntelliSense (Pylance), linting, debugging, code navigation, code formatting, refactoring, variable explorer, test explorer, and more!

## Installation de Docker et du plungin Compose ##
sur le site https://docs.docker.com/engine/install/ubuntu/ nous avons utilisé les instructions dinstallation de Docker sur Ubuntu en utilisant le repositoire apt. L´installation a été un succes facile et nous avons essayé notre premiere commande :
** sudo docker run hello-world **
qui telecharge l´image de ce conteneur et affiche ¨Hello World¨

pour gerer docker en tant qu´utilisateur non root sur Ubuntu, le système a créé automatiquement un groupe à l´installation du Docker Engine. il suffit d´ajouter notre profil utilisateur a ce groupe pour avoir les privilège necessaire pour executer Docker
sudo usermod -aG docker $USER

## Lancement de la phase 1: ##
Pour commencer, nous avons créé un dépôt dans GitHub pour la gestion de code et faire la connection entre ce compte avec une branche pour chaque membre de l´équipe.Ensuite, je l'ai cloné sur mon poste en local dans l'application VScode. Ensuite j'ai préparé mon environnement de développement en faisant les installations suivantes dans VsCode : 

# INSTALLER LE PACKAGE VIRTUAL ENVIRONMENT PYTHON3-VENV 
Avec VScode, nous avons créé un repertoire pour chaque conteneur, ce qui conduit à un pour
Mysql, un pour flask et un pour Nginx
dans chacun des repertoire nous avons un fichier dockerfile qui contient les parametres servant à la construction du conteneur dans docker.
Dans un premier temps j'ai créer  

Python :  

Flask : j'ai lu la documentation et lancé les commandes dans un terminal pour faire l'installation. Première commande 

sudo apt update
sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
sudo apt install python3-dev default-libmysqlclient-dev build-essential
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config
creation de l'environnement Python
sudo apt install python3-venv
python3 -m venv .venv 



GitHub Pull Requests and issues et Docker ont été ajouté à partir du module d'extension dans Vscode.

Dans un deuxième temps, j'ai lu la documentation sur Docker Compose pour pouvoir l'installer et commencer à l'utilisé. https://docs.docker.com/compose/install/linux/#install-using-the-repository
apt install python3.10-venv
apt-get isntall build-essential python-dev git

# CREATION DE L'ENVIRONNMENT VIRTUEL -m POUR MODULE
creation de l´environnement virtuel de python dans le repertoire flask
python3.10 -m venv .venv

# SELECTIONER L'INTERPRETER POUR L'ENV DE TRAVAIL
faire la combinaison des touches 

ctrl+shift+p  

dans vscode ou dans le menu de View -> Command Palette chercher 

python:select interpreter
puis choisir

"./.venv/bin/python"
cette action peut etre executer via le terminal de VScode par la commande:

source .venv/bin/activate

# INSTALLER FLASK et UWSGI
une fois dans l'environnement virtuel, nous pouvons installer les 
(.venv)$ pip install uwsgi flask
on tombe sur une error sans installer la version python3.10-dev

nous allons dans le repertoire flask pour creer  point d´entree du programme
creation du fichier app.py - app.py crée
nous creons aussi le repertoire app qui va contenir les fichiers python du programme, dans ce repertoire nous creons deux fichiers:
__init__.py   pour que Python considere notre repertoire comme contenant des paquets. il sert aussi à executer du code d´initialisation pour le paquet
views.py  : qui contient le corps du programme
le repertoire __pycache__ est creer autaumatiquement par python, nous avons ajouter un .dockerignore pour exclure les fichiers et repertoire de developpement
....

pour tester si uWSGI peut faire fonctionner le programme

uwsgi --socket localhost:5000 --protocol=http -w wsgi:app

# CREATE DOCKERFILE
docker image inspect <imageID> me donne les informations tel que la version d´un image du repo de docker

# CREATION DU FICHIER .FLASKENV
ce fichier dans le repertoire flask permet d'inserer les variables d'environnement de flask. 
# AJOUT DE SQLALCHEMY ORM DANS REQUIREMENTS ET RELANCER L'INSTALLATION

# CREATION DU FICHIER REQUIREMENTS (LISTE DES BIBLIOS UTILISEES)
pip freeze > requirements.txt


Pour créer une API en utilisant Flask et interagir avec une base de données MySQL, nous devons utiliser un ORM (Object-Relational Mapping) tel que SQLAlchemy pour faciliter les opérations de base de données. SQLAlchemy sera installé en utilisant les commandes suivantes :
pip install Flask-SQLAlchemy
pour creer une image  
docker build -t mysql_db .
pour tester le programme python
flask run

Dockerfile describe how to create and build a Docker image,
docker-compose is used to describe how to run Docker images as containers.
on cree le fichier compose.yaml, pour compiler le tout 

docker compose build

si tout est correct, on pase la commande
docker compose up

