from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_redis import FlaskRedis
from flask_wtf.csrf import CSRFProtect
from config import ProductionConfig
from logging.config import dictConfig
import logging
import os
import random
import time
import sys
import socket
from fluent import sender, event

from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor

from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource, SERVICE_INSTANCE_ID, SERVICE_NAME, SERVICE_VERSION, PROCESS_PID
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter, SimpleSpanProcessor
# je ne peux pas verifier si le trift est le bon
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.exporter import jaeger

from opentelemetry.sdk.trace.sampling import StaticSampler, Decision
# from opentelemetry.exporter.prometheus import PrometheusMetricsExporter
#from prometheus_client import start_http_server, Counter, Gauge

# Configure logging to FluentD
fluent_sender = sender.FluentSender('biblio_app', host='localhost', port=24224)

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default",
            },
            "fluentd": {
                "class": "logging.handlers.SocketHandler",
                "host": "localhost",
                "port": 24224,
            }
        },
        "root": {"level": "DEBUG", "handlers": ["console", "fluentd"]},
    }
)



# OpenTelemetry Configuration
resource = Resource(attributes={SERVICE_NAME: "biblio-backend"})

trace.set_tracer_provider(TracerProvider(resource=resource))


# Exporter for tracing with Jaeger
jaeger_exporter = JaegerExporter(
    
    # configure agent
    agent_host_name='localhost',
    agent_port=6831,
    # optional: configure also collector
    collector_endpoint='http://localhost:14268/api/traces?format=jaeger.thrift',
    # username=xxxx, # optional
    # password=xxxx, # optional
    # max_tag_value_length=None # optional
)


# jaeger_exporter = jaeger.JaegerSpanExporter(
#     service_name="my-helloworld-service",
#     agent_host_name="localhost",
#     agent_port=6831,
# )


# trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(jaeger_exporter))

# Create a BatchSpanProcessor and add the exporter to it
span_processor = BatchSpanProcessor(jaeger_exporter)

# add to the tracer
trace.get_tracer_provider().add_span_processor(span_processor)

#metric:
reader = PeriodicExportingMetricReader(ConsoleMetricExporter())
meterProvider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(meterProvider)


# Flask App and configurations
app = Flask(__name__)
app.config.from_object(ProductionConfig)
csrf = CSRFProtect(app)
db = SQLAlchemy(app)
redis_client = FlaskRedis(app)
# Check if the connection is successfully established or not
# Initialisation du logger

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__, True)

# Instrument Flask, SQLAlchemy, and Redis with OpenTelemetry
with app.app_context():
    try:
        FlaskInstrumentor().instrument_app(app)
        SQLAlchemyInstrumentor().instrument(engine=db.engine)
        RedisInstrumentor().instrument()

    except Exception as e:
        print('************ ERROR: %s ', e)
# Prometheus Metrics
# start_http_server(8000)  # Prometheus server on port 8000


with app.app_context():
    try:
        db.session.execute(text('SELECT 1'))
        print('\n\n---****** Connexion a Mysql reussie ******')
    except Exception as e:
        print('\n\n----------- Connexion echoue ! ERROR : ', e)

# Routes and Models import
from . import routes, models

# Log an example message to FluentD
logging.basicConfig(level=logging.INFO)
logging.info("Biblio application started successfully")
with tracer.start_as_current_span('foo'):
    print('Hello world!')
