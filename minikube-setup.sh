#!/bin/bash

ARCH=$(arch)

### installing Docker
sudo apt-get update -y
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
echo the script is now ready
echo manually run minikube start --vm-driver=docker --memory=6G --cni=calico to start minikube
## Install Kubectl tool
curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl

## Next, set the executable permission on it and move to /usr/local/bin

chmod +x kubectl
sudo mv kubectl /usr/local/bin/

## Verify the kubectl version, run

 kubectl version -o yaml

#Now that Minikube is installed, start a Kubernetes cluster using the following command:

minikube start --driver=docker

Start-Minikube-Cluster-Ubuntu-22-04

This command initializes a single-node Kubernetes cluster, and it might take a few minutes to download the necessary components.

Once the minikube has started, verify the status of your cluster, run

minikube status

Minikube-Status-Command-Output-Ubuntu-22-04
6) Interact with Your Minikube Cluster

Use kubectl to interact with your Minikube Kubernetes cluster. For example, you can check the nodes in your cluster:

kubectl get nodes
kubectl cluster-info

Kubectl-Cluster-Node-Info-Ubuntu-Minikube

Try to deploy a sample nginx deployment, run following set of commands.

kubectl create deployment nginx-web --image=nginx
kubectl expose deployment nginx-web --type NodePort --port=80
kubectl get deployment,pod,svc

Kubectl-Deploy-Nginx-SVC-Minikube-Ubuntu-22-04
7) Managing Minikube Addons

If you want to add some additional functionality toy Kubernetes cluster like Kubernetes dashboard, ingress controller and more. You can enable these with addons. To view all the available addons, run

minikube addons list

List-Minikube-addons-Ubuntu

In order to enable addons, run

minikube addons enable dashboard
minikube addons enable ingress

Enable-Minikube-Addons-Ubuntu-22-04

To start the Kubernetes dashboard run below command, it will automatically launch the dashboard in the web browser as shown below:

minikube dashboard

Starting-Kubernetes-Dashboard-Minikube

Kubernetes-Dashboard-GUI-Minikube-Ubuntu
8) Managing Minikube Cluster

To stop and start the minikube cluster, run beneath commands.

minikube stop
minikube start

In order to delete the minikube cluster, run

minikube delete




