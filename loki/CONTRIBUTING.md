Install the Docker driver client
The Docker plugin must be installed on each Docker host that will be running containers you want to collect logs from.

 docker plugin install grafana/loki-docker-driver:latest --alias loki --grant-all-permissions
 docker plugin ls

 ID: 13186