docker run -p 9090:9090 -v /prometheus-data prom/prometheus -config.file=/prometheus-data/prometheus.yml
with dockerfile:
docker build -t my-prometheus ./prometheus
docker run -dp 9090:9090 my-prometheus
