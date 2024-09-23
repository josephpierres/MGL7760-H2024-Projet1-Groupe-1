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
from prometheus_client import start_http_server, Counter, Gauge

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
        resource=Resource.create({"service.name": "biblio-backend"})
    )
)

# Exporter for tracing using OpenTelemetry Collector
otlp_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317")
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Instrumentation for Flask, SQLAlchemy, and Redis
FlaskInstrumentor().instrument_app(app)
SQLAlchemyInstrumentor().instrument(engine=db.engine)
RedisInstrumentor().instrument()

# Prometheus Metrics Exporter
metrics.set_meter_provider(MeterProvider())
exporter = PrometheusMetricsExporter()
start_http_server(port=8000)  # Expose metrics on port 8000

# Flask app setup
app = Flask(__name__)
app.config.from_object(ProductionConfig)
csrf = CSRFProtect(app)
db = SQLAlchemy(app)
redis_client = FlaskRedis(app)

# Health check for MySQL connection
with app.app_context():
    try:
        db.session.execute(text('SELECT 1'))
        print('--- MySQL connection successful ---')
    except Exception as e:
        print(f'--- MySQL connection failed: {e} ---')

# Routes and Models import
from . import routes, models

# Log startup message
logging.info("Biblio application started successfully")
