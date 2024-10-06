docker run -d -p 3000:3000 --name=grafana  -e "GF_LOG_LEVEL=debug" --volume grafana-storage:/var/lib/grafana  grafana/grafana-enterprise


http://localhost:3000/?orgId=1