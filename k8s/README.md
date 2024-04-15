These are the steps to create a MySQL instance inside Kubernetes

# 0. Go to mysql directory inside helm
`` kubectl -n bbl apply -k . ``
# 4. Install MySQL Helm Chart
``helm install -n bbl bbl-mysql ./mysql``
# installation de redis
``helm install -n bbl bbl-redis ./redis``
# installation de wsgi
``helm install -n bbl bbl-wsgi ./wsgi``
# installation de wsgi
``helm install -n bbl bbl-nginx ./nginx``



minikube service flask-nginx -n bbl


accer au pod mysql

kubectl get pods -n bbl

Choisissez le nom du pod MySQL que vous souhaitez accéder.

Utilisez la commande kubectl exec pour exécuter des commandes à l'intérieur du pod 


kubectl exec -it -n bbl flask-mysql-6f645c778-jbln8  -- /bin/bash

kubectl run -it --rm --image=mysql:8.3 --restart=Never mysql-client -- mysql -h mysql -password="password"

`` kubectl describe pod -n bbl app-7b6b68ccb8-g67q7  ``

mysql -ppassword 
use gestion_bibliotheque

helm delete bbl-wsgi -n bbl
kubectl delete pv --all -n bbl
kubectl delete pvc --all -n bbl
kubectl delete sc --all -n bbl

image: repository:organization_name/image_name:image_version


kubectl logs app-844f8df59f-57875  -n bbl -p

kubectl exec -it -n bbl web-bff778fb8-bxwft -- /bin/bash


As the handbook describes, you can reuse the Docker daemon from Minikube with eval $(minikube docker-env).
https://minikube.sigs.k8s.io/docs/handbook/pushing/#1-pushing-directly-to-the-in-cluster-docker-daemon-docker-env

So to use an image without uploading it, you can follow these steps:

Set the environment variables with eval $(minikube docker-env)
Build the image with the Docker daemon of Minikube (e.g., docker build -t my-image .)
Set the image in the pod specification like the build tag (e.g., my-image)
Set the imagePullPolicy to Never, otherwise Kubernetes will try to download the image.
Important note: You have to run eval $(minikube docker-env) on each terminal you want to use, since it only sets the environment variables for the current shell session.


# Start minikube
minikube start

# Set docker env
eval $(minikube docker-env)             # Unix shells
minikube docker-env | Invoke-Expression # PowerShell

# Build image
sudo docker build -t bbl-wsgi ./data/wsgi
minikube image build -t localhost:5000/bbl-wsgi ./data/wsgi

# Load the image into Minikube
minikube image load bbl-wsgi
minikube cache reload
minikube cache list
minikube cache delete <image name>

# Run in Minikube
kubectl run bbl-wsgi --image=wsgi:1.0.3 --image-pull-policy=Never

# Check that it's running
kubectl get pods

minikube service nginx-service