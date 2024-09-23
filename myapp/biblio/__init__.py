# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import text
# from flask_redis import FlaskRedis
# from flask_wtf.csrf import CSRFProtect
# from config import ProductionConfig
# from logging.config import dictConfig
# import logging
# import os
# import random
# import time
# import sys
# import socket
# from fluent import sender, event

# from opentelemetry.instrumentation.flask import FlaskInstrumentor
# from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
# from opentelemetry.instrumentation.redis import RedisInstrumentor

# from opentelemetry import metrics
# from opentelemetry.sdk.metrics import MeterProvider
# from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader
# from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter

# from opentelemetry import trace
# from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
# from opentelemetry.sdk.resources import Resource, SERVICE_INSTANCE_ID, SERVICE_NAME, SERVICE_VERSION, PROCESS_PID
# from opentelemetry.sdk.trace import TracerProvider
# from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter, SimpleSpanProcessor
# # je ne peux pas verifier si le trift est le bon


# from opentelemetry.sdk.trace.sampling import StaticSampler, Decision
# # from opentelemetry.exporter.prometheus import PrometheusMetricsExporter
# #from prometheus_client import start_http_server, Counter, Gauge


import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_redis import FlaskRedis
from flask_wtf.csrf import CSRFProtect
from config import ProductionConfig
from logging.config import dictConfig
import logging
from fluent import sender, event
from opentelemetry import trace, metrics
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.prometheus import PrometheusMetricsExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.metrics import MeterProvider
from prometheus_client import start_http_server

from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.exporter import jaeger



# Configure logging to FluentD
fluent_sender = sender.FluentSender('biblio_app', host='localhost', port=24224)

dictConfig({
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
})

# OpenTelemetry configuration for tracing
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({"service.name": "wsgi"})
    )
)

# Exporter for tracing using OpenTelemetry Collector
otlp_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317")
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)



# Prometheus Metrics Exporter
metrics.set_meter_provider(MeterProvider())
exporter = PrometheusMetricsExporter()
start_http_server(port=8000)  # Expose metrics on port 8000


#########################################################
# Exporter for tracing with Jaeger
jaeger_exporter = JaegerExporter(
    
    # configure agent
    agent_host_name='localhost',
    agent_port=6831,
    # optional: configure also collector
    #collector_endpoint='http://localhost:14268/api/traces?format=jaeger.thrift',
    # username=xxxx, # optional
    # password=xxxx, # optional
    # max_tag_value_length=None # optional
)
# Create a BatchSpanProcessor and add the exporter to it
span_processor = BatchSpanProcessor(jaeger_exporter)

# add to the tracer
trace.get_tracer_provider().add_span_processor(span_processor)

####################################################################



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
        # Instrumentation for Flask, SQLAlchemy, and Redis

        FlaskInstrumentor().instrument_app(app)
        SQLAlchemyInstrumentor().instrument(engine=db.engine)
        RedisInstrumentor().instrument()
   
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

# Sending a custom log message using fluent_sender
fluent_sender.emit('app.event', {
    'message': 'Custom log message from Fluentd sender',
    'service': 'biblio-backend',
    'status': 'success',
    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
})