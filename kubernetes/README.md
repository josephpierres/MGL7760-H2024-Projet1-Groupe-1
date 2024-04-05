These are the steps to create a MySQL instance inside Kubernetes

# 0. Go to mysql directory inside helm
``cd helm/mysql``

# 1. Create 'bbl' namespace
``kubectl create -f namespace-bbl.yaml``

# 2. Create a storage class
``kubectl -n bbl apply -f sc-mysql.yaml``

# 3. Create the persistent volume
``kubectl -n bbl apply -f pv-mysql.yaml``

# 4. Install MySQL Helm Chart
``helm install --namespace bbl bbl-mysql .``

# 5. For subsequent releases, run helm upgrade
``helm upgrade --namespace bbl bbl-mysql .``

# --------------------------------------------------------------------------
In helm directory, do these steps to install Nginx PHP-FPM inside Kubernetes
# 6. Create the app (Nginx-PHP) storage class
``kubectl -n bbl apply -f sc-app.yaml``

# 7. Create the persistent volume to store app data
``kubectl -n bbl apply -f pv-app.yaml``

# 8. Install PHP-FPM Helm Chart
``helm install --namespace bbl bbl-php ./php``

# 9. Install Nginx Helm Chart
``helm install --namespace bbl bbl-nginx ./nginx``

This is a screenshort of the deployments:
![Deployments](deployments.png "Deployments")