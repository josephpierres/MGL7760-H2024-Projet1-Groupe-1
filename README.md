Je reprend le devoir de la Session	Hiver 2024
Sigle	MGL7760
Groupe	01
Crédits	3
Titre	Qualité et productivité des outils logiciels
Projet 1 : creation d'une base de donnee de gestion de Bibliotheque 
c'est un projet d'une application en python-flask-wsgi avec Mysql pour les bases de donnees et Nginx pour le serveur Web de presentation de l'application.
Le projet se lancait sur le port 8000 de Nginx http://localhost:8000 et affichait la liste de livre etc..

Pour le projet 1 du cour MGL870-01 Sujets spéciaux II : génie logiciel (A2024)
TP 1 - Mise en Œuvre un Pipeline Journalisation, du Traçage et des Métriques avec OpenTelemetry
Dont l'objectif de ce travail pratique (TP) en équipe est de fournir aux étudiants une expérience pratique de l'utilisation d'OpenTelemetry pour mettre en œuvre la journalisation, le traçage et la collecte de métriques au sein d'une application basée sur des services. Cet exercice aidera les étudiants à comprendre comment instrumenter leurs applications pour l'observabilité et comment analyser les données collectées pour obtenir des informations sur les performances et le comportement du système.
Nous avons choisi les technologies suivantes pour le pipeline

Architecture du Pipeline
L'architecture que vous avez mise en place pour le pipeline d'observabilité est un système distribué et intégré qui permet de surveiller, collecter et analyser des métriques, des journaux (logs), et des traces. Chaque composant joue un rôle important pour assurer le bon fonctionnement et la visibilité de votre application, de la base de données aux alertes.

Voici une description détaillée de chaque composant et son rôle dans le pipeline :

1. Biblio-app (wsgi) (http://localhost:8081/)
Rôle : Front-end de l'application.
Fonctionnement : Il s'agit d'une application Flask (ou un autre framework) déployée via WSGI. Elle sert les pages HTML et gère les interactions utilisateur à travers une interface graphique. Le front-end communique avec l'API pour envoyer/recevoir des données et s'intègre avec le reste de l'infrastructure pour l'observabilité (par exemple, des métriques peuvent être envoyées à Prometheus, des journaux à Loki, et des traces à Tempo/Jaeger via OpenTelemetry).
2. Biblio-api (http://localhost:8082/)
Rôle : Back-end de l'application.
Fonctionnement : Le back-end (FastAPI, Flask ou autre) gère les requêtes des clients. Il traite les données métiers et interagit avec la base de données MySQL et Redis. Les métriques de performance, les traces des requêtes, et les journaux d'activités sont envoyés vers les services d'observabilité (Prometheus, Loki, Tempo/Jaeger).
3. MySQL (0.0.0.0:3306)
Rôle : Base de données relationnelle.
Fonctionnement : MySQL stocke les données persistantes de l'application, telles que les informations sur les utilisateurs, les livres, les transactions, etc. Les traces de requêtes SQL peuvent être envoyées à Jaeger/Tempo pour être tracées. Les métriques de performance de MySQL peuvent être envoyées à Prometheus pour surveiller son état de santé.
4. Redis
Rôle : Cache de données et gestion des files d'attente.
Fonctionnement : Redis est utilisé pour stocker temporairement des données dans un cache rapide ou pour gérer des tâches asynchrones. Il permet d'améliorer la vitesse des réponses de l'application. Des métriques liées aux performances de Redis (telles que les latences et le nombre de requêtes) sont collectées et envoyées à Prometheus.
5. Nginx (http://localhost:8000)
Rôle : Serveur web et répartiteur de charge (load balancer).
Fonctionnement : Nginx gère les requêtes HTTP et les distribue aux différentes instances de l'application back-end (Biblio-api). Il peut également gérer la mise en cache et l'équilibrage de charge. Les journaux d'accès et d'erreurs sont envoyés à Loki, et ses métriques de performance sont collectées par Prometheus.
6. Grafana (http://localhost:3000/)
Rôle : Interface utilisateur pour la visualisation des traces, métriques, et journaux.
Fonctionnement : Grafana permet de créer des tableaux de bord pour visualiser les métriques (issues de Prometheus), les traces (issues de Tempo ou Jaeger), et les journaux (issues de Loki). Cela offre une vue unifiée sur l'état de santé et la performance de l'infrastructure.
7. Jaeger UI (http://localhost:16686/)
Rôle : Interface utilisateur pour visualiser les traces distribuées.
Fonctionnement : Jaeger stocke et visualise les traces distribuées des requêtes effectuées sur votre application. Il permet de suivre une requête à travers plusieurs services (Biblio-api, MySQL, Redis, etc.) et de détecter les points de latence ou d'erreurs dans ces services.
8. Prometheus (http://localhost:9090/)
Rôle : Système de collecte et stockage des métriques.
Fonctionnement : Prometheus collecte les métriques de performance depuis divers services (Nginx, Redis, Biblio-api, etc.) via des sondes ou des intégrations. Il permet de définir des règles d'alerte en fonction de seuils critiques et d'envoyer ces alertes à AlertManager.
9. OpenTelemetry Collector
Rôle : Centralisation et traitement des données d'observabilité (traces, métriques, journaux).
Fonctionnement : OpenTelemetry Collector collecte des données de différents services (Biblio-api, Redis, MySQL), les normalise, et les envoie vers Jaeger (pour les traces), Loki (pour les logs), et Prometheus (pour les métriques). Il agit comme un pipeline centralisé pour l'observabilité.
10. Loki
Rôle : Stockage des journaux.
Fonctionnement : Loki collecte et stocke les journaux (logs) générés par les services comme Nginx, Biblio-api, ou Redis. Il permet de centraliser l'analyse des journaux dans Grafana, où ces logs peuvent être corrélés avec des métriques et des traces.
11. Tempo
Rôle : Stockage des traces distribuées.
Fonctionnement : Tempo est utilisé pour stocker les traces distribuées envoyées par OpenTelemetry. Il fonctionne de manière similaire à Jaeger mais est optimisé pour des scénarios où la performance et le stockage à grande échelle des traces sont nécessaires.
12. AlertManager (http://localhost:9093/)
Rôle : Gestion des alertes.
Fonctionnement : AlertManager reçoit les alertes provenant de Prometheus. Il gère la déduplication, le routage, et l'envoi des notifications d'alerte aux équipes concernées (via email, Slack, etc.) lorsqu'un seuil critique est atteint (par exemple, un service en panne ou une base de données sous forte charge).
Fonctionnement global :
Collecte des données : OpenTelemetry collecte des métriques, traces, et journaux des services (front-end, back-end, base de données, cache, etc.) et les centralise dans OpenTelemetry Collector.

Stockage et visualisation :

Traces : Envoyées à Jaeger ou Tempo pour être stockées et analysées.
Métriques : Stockées dans Prometheus et visualisées dans Grafana.
Journaux : Envoyés à Loki pour être centralisés et analysés dans Grafana.
Alertes : Si des anomalies sont détectées (par exemple des seuils critiques définis dans Prometheus), AlertManager envoie des notifications aux administrateurs pour qu'ils puissent intervenir rapidement.

Cette architecture offre une surveillance complète et une visibilité unifiée sur les performances, l'état de santé, et les événements dans le système.

## Démarrage rapide

Démarrage rapide du projet
Voici un guide rapide pour démarrer le projet en utilisant les services et technologies mentionnés. Ce guide inclut les étapes de configuration et d'exécution des différents services.

Prérequis
Docker et Docker Compose installés
Familiarité avec les concepts de conteneurs et d'outils comme Nginx, Prometheus, Loki, Jaeger, etc.
Étapes de démarrage rapide
1. Cloner le dépôt du projet
Si votre projet est hébergé sur GitHub ou un autre service, clonez-le sur votre machine locale :

bash
Copy code
git clone https://github.com/username/biblio-project.git
cd biblio-project
2. Configurer Docker Compose
Le fichier docker-compose.yml doit être configuré pour inclure tous les services que vous utilisez : front-end, back-end, base de données, Redis, Nginx, OpenTelemetry Collector, Prometheus, Grafana, Jaeger, Loki, Tempo, et AlertManager.

Vérifiez que chaque service a les bons ports et les dépendances correctes entre les services.

3. Exécuter Docker Compose
Pour démarrer tous les services en même temps, utilisez la commande suivante dans le répertoire où se trouve votre fichier docker-compose.yml :

bash
Copy code
docker-compose up --build
Cette commande construira et démarrera les conteneurs pour tous les services. Les services seront accessibles via les URLs et ports que vous avez définis (par exemple, http://localhost:8081 pour le front-end, http://localhost:8082 pour le back-end).

4. Accéder aux services
Front-end : http://localhost:8081/
Back-end (API) : http://localhost:8082/
Base de données (MySQL) : 0.0.0.0:3306
Redis : 0.0.0.0:6379
Nginx : http://localhost:8000/
Grafana : http://localhost:3000/ (identifiants par défaut : admin/admin)
Jaeger UI : http://localhost:16686/
Prometheus : http://localhost:9090/
AlertManager : http://localhost:9093/
Loki : Collecte et stockage des journaux
Tempo : Collecte et stockage des traces
5. Vérifier les services
Vérifier les logs : Vous pouvez visualiser les logs des services avec Docker en utilisant docker-compose logs. Par exemple :

bash
Copy code
docker-compose logs nginx
Vérifier les métriques et traces : Ouvrez Grafana (http://localhost:3000/) et configurez des tableaux de bord pour visualiser les métriques provenant de Prometheus, les traces de Tempo, et les journaux de Loki.

6. Alertes et Surveillance
AlertManager surveillera les métriques envoyées par Prometheus. Si un service dépasse un seuil critique (CPU, mémoire, etc.), une alerte sera envoyée via AlertManager. Configurez les notifications (Slack, Email, etc.) pour être averti en cas de problèmes.
7. Interaction avec l'API et la base de données
Utilisez MySQL (http://localhost:3306) pour vérifier ou gérer les données stockées par l'application.
Vous pouvez également tester les routes du back-end avec des outils comme Postman ou cURL.
8. Tests et développement
Pendant que le pipeline est en cours d'exécution, vous pouvez commencer à tester les différentes fonctionnalités de l'application, surveiller les métriques de performance, et analyser les traces distribuées via Jaeger ou Tempo.

Commandes utiles
Redémarrer les services :

bash
Copy code
docker-compose restart
Arrêter les services :

bash
Copy code
docker-compose down
Vérifier les logs d'un service spécifique :

bash
Copy code
docker-compose logs <nom_du_service>
Conclusion
En suivant ces étapes, vous aurez rapidement un environnement complet fonctionnant avec tous les services d'observabilité et d'application en cours d'exécution. Vous pourrez ensuite commencer à tester les fonctionnalités, analyser les performances, et surveiller la santé globale de votre application grâce à Grafana, Jaeger, Loki, et Prometheus.

## Comment cela fonctionne

Recherchez la demande dans l'interface utilisateur :
- Ouvrez [`Grafana`](http://localhost:3000/explore), sélectionnez `Tempo`, passez au type de requête `Recherche` et cliquez sur `Exécuter la requête` :
 ![grafana_explore_traces](./images/grafana_explore_traces1.png)
- Ouvrez [`Jaeger UI`](http://localhost:16686/), sélectionnez le service dans `Services` et cliquez sur `Find Traces` :
 ![jaeger_expore_traces](./images/jaeger_expore_traces1.png)

Ouvrez la trace de la requête et obtenez toutes les informations sur les spans :
- Grafana :
 ![grafana_show_trace](./images/grafana_show_trace.png)
- Interface utilisateur Jaeger :
 ![jaeger_show_trace](./images/jaeger_show_trace.png)

 Tester avec siege (siege request-script)
 Le script que nous avons utilisé avec Siege effectue une série de tests de charge sur différentes routes de votre application en simulant plusieurs utilisateurs simultanés envoyant des requêtes HTTP. Chaque test évalue la capacité du système à répondre à différentes requêtes avec des charges spécifiques.
 Ce script effectue un test de charge sur plusieurs routes de votre application en utilisant différentes configurations de charge (nombre d'utilisateurs simultanés et nombre de requêtes par utilisateur). Cela permet de simuler divers scénarios d'utilisation pour évaluer les performances et la robustesse de votre application sous différentes conditions de charge.

L'objectif est de vérifier la capacité de l'application à gérer plusieurs requêtes simultanées sur différentes routes, identifier les éventuels points de latence, et s'assurer que le système reste stable même sous une charge modérée à forte.

Arrêter les services
```
docker-compose down -v

