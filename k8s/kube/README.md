These are the steps to create a MySQL instance inside Kubernetes

# 0. Go to mysql directory inside helm
`` kubectl -n bbl apply -k . ``
# 4. Install MySQL Helm Chart
``helm install -n bbl bbl-mysql ./mysql``
# installation de redis
``helm install -n bbl bbl-redis ./redis``
# installation de wsgi


kubectl -n bbl apply -k . 
helm install -n bbl bbl-wsgi ./wsgi
kubectl get pods -n bbl
helm install -n bbl bbl-nginx ./nginx
kubectl get pods -n bbl


helm upgrade -n bbl bbl-wsgi ./wsgi


helm upgrade -n bbl bbl-nginx ./nginx

kubectl delete  configmap nginx-config -n bbl 
helm delete bbl-nginx -n bbl


helm delete bbl-wsgi -n bbl
kubectl delete  pv app-pv -n bbl  

kubectl delete  pvc app-pvc -n bbl 
kubectl delete  sc app-sc -n bbl  
kubectl delete  configmap uwsgi-config -n bbl   


helm upgrade -n bbl bbl-wsgi ./wsgi


minikube service flask-nginx -n bbl


accer au pod mysql

kubectl get pods -n bbl

Choisissez le nom du pod MySQL que vous souhaitez accéder.

Utilisez la commande kubectl exec pour exécuter des commandes à l'intérieur du pod 


kubectl exec -it -n bbl flask-nginx-f4b547456-hzdvn  -- /bin/bash

kubectl run -it --rm --image=mysql:8.3 --restart=Never mysql-client -- mysql -h mysql -password="password"

`` kubectl describe pod -n bbl nginx-biblio-64f6ff75fb-cxz68  ``

mysql -ppassword 
use gestion_bibliotheque


kubectl delete pv --all -n bbl
kubectl delete pvc --all -n bbl
kubectl delete sc --all -n bbl


kubectl describe pod -n bbl app

image: repository:organization_name/image_name:image_version


```   kubectl logs nginx-biblio-64f6ff75fb-g8mf8   -n bbl -p    ``

kubectl exec -it -n bbl nginx-biblio-64f6ff75fb-z6xzs -- /bin/bash


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

### pour creer l'image que nous avons besoin dans minikube
eval $(minikube docker-env)
minikube image build -t biblio-wsgi:1.0.0 ./data/wsgi 

# Load the image into Minikube
minikube image load bbl-wsgi
minikube cache reload
minikube cache list
minikube cache delete <image name>

# Run in Minikube
kubectl run bbl-wsgi --image=wsgi:1.0.3 --image-pull-policy=Never

# Check that it's running
kubectl get pods

minikube service nginx-biblio-service -n bbl

 kubectl logs -f -n bbl nginx-biblio-64f6ff75fb-z6xzs

uwsgi --socket 0.0.0.0:8001 --protocol=http -w wsgi:main