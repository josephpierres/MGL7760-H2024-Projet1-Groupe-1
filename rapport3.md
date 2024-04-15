kubectl get pods | grep sas-mi pour trouver le tag de 
kubectl -n $GELENV_NS get pods | grep microanalytic | awk 'NR==1{print $1}'

Installation de minikube et kubectl

# apres install
kubectl completion -h 
# on trouve les code de completion
# ensuite, creation de nginx avec exemple
kubectl run -h | less  
kubectl run nginx --image=nginx


---- BEGIN SSH2 PUBLIC KEY ----
Comment: "rsa-key-20240320"
AAAAB3NzaC1yc2EAAAADAQABAAABAQCMLiXNm8FtXFnoFXmAw6A4lRnWv3XdCMvj
GxMNZPM2FvUoLxGS0fm8P6KPPPbxtZK6Ze+c7vLS/R1CxzjL9McCwSopa8SmqPEq
nqWei48m3DfqfNIvAQqywawQycdG9DqNL71plLcoFT202M6EvCMbIaWCAGLYa4GB
IJ5eaw235MECowa7bHNCiaGlUO2JqGfoTGRuDsXOxZDvW6cfLMEUGhTj+qRiBceV
mnf4nC3ZtsmaBSwXOCxnLA6KvFSruVUzXCmVjMk+EaohGv39zmD/kF1NrraAX8BZ
cr/G9pa6qrHFVY+/qXxe6SBkP3f4zkEV+SBl7hVu0G9zcpBUBMNL
---- END SSH2 PUBLIC KEY ----


kubectl config get get-contexts set-context use-context  context_name --namespace=nom_namespace

j'ai une erreur dans la commande
helm install nginx01 bitnami/nginx dans le namespace web
correction:
export KUBECONFIG=~/.kube/config

helm install mysql-chart ./mysql-chart --namespace bbl --values values.yaml.


pipeline {
    agent any
    environment {
        KUBECONFIG = credentials('kubernetes-config')
    }
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/kubernetes/ingress-nginx.git'
            }
        }
        stage('Deploy Helm chart') {
            steps {
                sh "helm install ingress-nginx ./deploy/charts/ingress-nginx --namespace ingress-nginx --set controller.publishService.enabled=true --set controller.service.loadBalancerIP=${env.LB_IP}"
            }
        }
    }
}





helm ls --all-namespace
helm uninstall <package> --namespace=bbl