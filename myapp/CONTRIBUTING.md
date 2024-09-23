How It Works:
Jaeger: Your application traces will be sent to OpenTelemetry Collector, which forwards them to Jaeger for visualization. You can access Jaeger at http://localhost:16686.
Prometheus: Metrics from your app will be exposed at http://localhost:8000 and can be collected by Prometheus.
Fluentd: Logs from Biblio, MySQL, Nginx, and Redis will be forwarded to Fluentd and saved into log files or output to stdout.

Steps to integrate Grafana:
Add Grafana to the docker-compose.yml file and configure it to use Prometheus as a data source for metrics and Jaeger for traces.
Configure Prometheus as the metrics collection system for the application and Grafana.
Update Fluentd configuration to log service-specific logs for better observability.
Add pre-configured Grafana dashboards for application metrics and traces visualization.


Prometheus Configuration (prometheus.yml)
We need to configure Prometheus to scrape metrics from your Flask application (exposed at localhost:8000) and system services like MySQL, Redis, and Fluentd.

OpenTelemetry Collector Configuration (otel-collector-config.yaml)
This configuration is for OpenTelemetry Collector to receive traces and export them to Jaeger, while also exporting metrics to Prometheus.

Fluentd Configuration (fluentd.conf)
To collect logs from all services in Docker Compose and forward them to Grafana, configure Fluentd with proper input and output sources.

Grafana Configuration
Accessing Grafana: Once Grafana is running, you can access it via http://localhost:3000 with the default login credentials:

Username: admin
Password: admin
Add Data Sources:

Prometheus (for metrics):

Go to Configuration > Data Sources and add a new data source.
Select Prometheus.
Set the URL to http://prometheus:9090.
Click Save & Test.
Jaeger (for traces):

Go to Configuration > Data Sources and add a new data source.
Select Jaeger.
Set the URL to http://jaeger:16686.
Click Save & Test.
Import Dashboards:

Grafana has pre-built dashboards for both Prometheus and Jaeger.
Go to Create > Import and enter the dashboard ID from Grafana's public repository:
Prometheus Flask Metrics: Use dashboard ID 1860 for Flask applications.
Jaeger Traces Dashboard: Use dashboard ID 13649 for Jaeger trace visualizations.



Accessing Grafana Dashboards:
Metrics Dashboard:

Open Grafana at http://localhost:3000.
Navigate to the Prometheus Flask Metrics Dashboard or any other dashboard for metrics.
Tracing Dashboard:

You can view Jaeger traces in Grafana after configuring the Jaeger data source.
Custom Dashboards:

You can create custom dashboards for Redis, MySQL, and Flask application metrics by querying Prometheus and visualizing the data in Grafana.


Testing and Monitoring:
Prometheus will collect metrics from:

The Flask application exposed at /metrics on port 8000.
MySQL and Redis metrics exporters.
Jaeger will visualize traces collected via the OpenTelemetry Collector.

Fluentd will aggregate logs from all services and store them for analysis.



we now have a full observability stack with Grafana for dashboards, Prometheus for metrics, Jaeger for traces, and Fluentd for logs. This setup gives you comprehensive monitoring and logging for your application, enabling real-time visualization of metrics and traces across the services.











OTEL_RESOURCE_ATTRIBUTES=service.name=flask-app \
OTEL_EXPORTER_OTLP_ENDPOINT="https://ingest.{region}.signoz.cloud:443" \
OTEL_EXPORTER_OTLP_HEADERS="signoz-access-token=SIGNOZ_INGESTION_KEY" \
OTEL_EXPORTER_OTLP_PROTOCOL=grpc \
opentelemetry-instrument python app.py



python3 -m venv .venv 
source ./.venv/bin/activate
pip3 install -r requirements.txt



alembic
backports-abc
blinker
click
Flask
Flask-Bootstrap
Flask-Login
Flask-Mail
Flask-Migrate
Flask-Moment
Flask-Script
Flask-SQLAlchemy
Flask-WTF
mysqlclient
itsdangerous
Jinja2
livereload
Mako
MarkupSafe
meld3
python-editor
singledispatch
six
gunicorn
SQLAlchemy
supervisor
tornado
uWSGI
Werkzeug


mysqlclient
pycrypto
PyMySQL
redis
requests
shellescape
simplejson



# Dockerfile:

FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /base_directory
WORKDIR /base_directory
ADD . /base_directory/
RUN apt-get update
RUN apt-get install -y git
RUN git init
RUN apt-get install -y gcc python3-dev
RUN apt-get install -y libxml2-dev libxslt1-dev build-essential python3-lxml zlib1g-dev
RUN apt-get install -y default-mysql-client default-libmysqlclient-dev
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN  python3 get-pip.py
RUN rm get-pip.py
RUN pip install -r requirements.txt
CMD start.sh


#!/bin/bash
nohup redis-server &
uwsgi --http 0.0.0.0:8000 --module mymodule.wsgi