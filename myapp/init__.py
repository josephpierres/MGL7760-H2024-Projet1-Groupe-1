# import datetime
# import logging
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import text
# from flask_redis import FlaskRedis
# from flask_wtf.csrf import CSRFProtect
# from config import ProductionConfig

# # OpenTelemetry imports
# from opentelemetry import trace, metrics
# from opentelemetry.sdk.resources import Resource
# from opentelemetry.sdk.trace import TracerProvider

# from opentelemetry.sdk.metrics import MeterProvider
# from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
# from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
# from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

# from opentelemetry._logs import set_logger_provider


# from opentelemetry.exporter.otlp.proto.grpc._log_exporter import (
#     OTLPLogExporter,
# )
# from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
# from opentelemetry.sdk._logs.export import BatchLogRecordProcessor


# from opentelemetry.sdk.trace.export import (
#     BatchSpanProcessor,
#     ConsoleSpanExporter,
# )
# from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
# from opentelemetry.instrumentation.flask import FlaskInstrumentor
# from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
# from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

# from pythonjsonlogger import jsonlogger
# # Flask App and configurations
# app = Flask(__name__)


# # Initialize OpenTelemetry Tracer and Meter
# resource = Resource(attributes={
#     "service.name": "wsgi",
#     "service.version": "1.0.0"
# })

# # Tracer setup
# trace_provider = TracerProvider(resource=resource)
# trace_exporter = OTLPSpanExporter(endpoint="localhost:4317", insecure=True)
# trace_provider.add_span_processor(BatchSpanProcessor(trace_exporter))
# trace.set_tracer_provider(trace_provider)

# # Metrics setup
# metric_exporter = OTLPMetricExporter(endpoint="localhost:4317", insecure=True)
# meter_provider = MeterProvider(
#     resource=resource,
#     metric_readers=[PeriodicExportingMetricReader(metric_exporter)]
# )
# metrics.set_meter_provider(meter_provider)

# # Logger setup
# logger_provider = LoggerProvider(resource=resource)
# set_logger_provider(logger_provider)
# log_exporter = OTLPLogExporter(endpoint="localhost:4317", insecure=True)
# logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))

# #  console_exporter = ConsoleLogExporter()
# #  logger_provider.add_log_record_processor(BatchLogRecordProcessor(console_exporter))



# # Attach a logging handler that sends logs to OTLP
# # handler = logging.StreamHandler()
# handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
# app.logger.addHandler(handler)

# # handler.setLevel(logging.DEBUG)
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# tracer = trace.get_tracer(__name__)
# meter = metrics.get_meter(__name__)

# with app.app_context():
#     # Instrument Flask, SQLAlchemy, and Redis with OpenTelemetry
#     FlaskInstrumentor().instrument_app(app)
#     SQLAlchemyInstrumentor().instrument(engine=db.engine)
#     RedisInstrumentor().instrument()
    #   RequestsInstrumentor().instrument()     
#     # Check if the connection is successfully established or not

#     try:
#         db.session.execute(text('SELECT 1'))
#         print('\n---****** Connexion à MySQL réussie ******')
#     except Exception as e:
#         print('\n----------- Connexion échouée ! ERROR : ', e)

# # Routes and Models import
# from . import routes, models

# # Example span creation

# with tracer.start_as_current_span('example-span'):
#     logger.info("Starting example span")

# # Example custom log message
# logger.info("WSGI service started successfully")

# # Obtenir le meter pour les métriques





# # # Définir un compteur pour compter le nombre de requêtes traitées
# # request_counter = meter.create_counter(
# #     name="http_requests_total",
# #     description="Total number of HTTP requests",
# #     unit="requests"
# # )
# # request_counter.add(1, {"endpoint": "/some-endpoint", "method": "GET"})



# # # Create different namespaced loggers
# # # It is recommended to not use the root logger with OTLP handler
# # # so telemetry is collected only for the application
# # logger1 = logging.getLogger("myapp.area1")
# # logger2 = logging.getLogger("myapp.area2")

# # logger1.debug("Quick zephyrs blow, vexing daft Jim.")
# # logger1.info("How quickly daft jumping zebras vex.")
# # logger2.warning("Jail zesty vixen who grabbed pay from quack.")
# # logger2.error("The five boxing wizards jump quickly.")


# # # Trace context correlation

# # with tracer.start_as_current_span("foo"):
# #     # Do something
# #     logger2.error("Hyderabad, we have a major problem.")

# # logger_provider.shutdown()


import json
import logging
import os
from random import randint
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_redis import FlaskRedis
from flask_wtf.csrf import CSRFProtect
from config import ProductionConfig


from opentelemetry.sdk.resources import Resource

# Import exporters
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import ( OTLPLogExporter,)


# Trace imports
from opentelemetry import trace
from opentelemetry.trace import set_tracer_provider, get_tracer_provider
from opentelemetry.sdk.trace import TracerProvider, sampling
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Metric imports
from opentelemetry import metrics as metrics
from opentelemetry.sdk.metrics.export import (  AggregationTemporality,  PeriodicExportingMetricReader,)
from opentelemetry.sdk.metrics import MeterProvider, Counter, UpDownCounter, Histogram, ObservableCounter, ObservableUpDownCounter
from opentelemetry.metrics import set_meter_provider, get_meter_provider

# Logs import
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry._logs import set_logger_provider


from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor


resource = Resource.create(
        {
            "service.name": "demo-dice",
            "service.instance.id": "demo-dice",
        }
    )

# create the log providers ****

logger_provider = LoggerProvider(resource=resource)

# set the  providers

set_logger_provider(logger_provider)

log_exporter = OTLPLogExporter(endpoint=os.getenv("OTLP_ENDPOINT", "localhost:4317"), insecure=json.loads(os.getenv("INSECURE", "true").lower()))

# add the batch processors to the trace provider
logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))


handler = LoggingHandler(level=logging.DEBUG,logger_provider=logger_provider)
# Create different namespaced loggers

logger = logging.getLogger("myapp.area2")
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


# create the trace providers *********
tracer_provider = TracerProvider(resource=resource)

# set the providers
set_tracer_provider(tracer_provider)

trace_exporter = OTLPSpanExporter(
    endpoint=os.getenv("OTLP_ENDPOINT", "http://otelcol:4317"), 
   # insecure=json.loads(os.getenv("INSECURE", "true").lower()),
    )

span = BatchSpanProcessor(trace_exporter)
tracer_provider.add_span_processor(span)

tracer = get_tracer_provider().get_tracer("my-tracer")

# create the metric providers *****************

exporter = OTLPMetricExporter( endpoint=os.getenv("OTLP_ENDPOINT", "localhost:4318"), 
                              insecure=json.loads(os.getenv("INSECURE", "true").lower()),
                              preferred_temporality = {
                                    Counter: AggregationTemporality.DELTA,
                                    UpDownCounter: AggregationTemporality.CUMULATIVE,
                                    Histogram: AggregationTemporality.DELTA,
                                    ObservableCounter: AggregationTemporality.DELTA,
                                    ObservableUpDownCounter: AggregationTemporality.CUMULATIVE,
                                }
                            )
reader = PeriodicExportingMetricReader(exporter)
provider = MeterProvider(metric_readers=[reader], resource=resource)
set_meter_provider(provider)
meter = get_meter_provider().get_meter("my-meter", "0.1.2")

app = Flask(__name__)
app.logger.addHandler(handler)
app.config.from_object(ProductionConfig)

# Initialize CSRF protection, database, and Redis
csrf = CSRFProtect(app)
db = SQLAlchemy(app)
redis_client = FlaskRedis(app)

# handler.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)

with app.app_context():
    # # Instrument Flask, SQLAlchemy, and Redis with OpenTelemetry
    # FlaskInstrumentor().instrument_app(app)
    # SQLAlchemyInstrumentor().instrument(engine=db.engine)
    # RedisInstrumentor().instrument()
    # RequestsInstrumentor().instrument()     
    # Check if the connection is successfully established or not

    try:
        db.session.execute(text('SELECT 1'))
        print('\n---****** Connexion à MySQL réussie ******')
    except Exception as e:
        print('\n----------- Connexion échouée ! ERROR : ', e)

# Routes and Models import
from . import routes, models

# @app.route("/rolldice")
# def roll_dice():
#     final_roll = str(do_roll())
#     args = request.args
#     user = args.get('user',  "anonymous")
#     logger2.info("completed request for user: " + user + "with dice roll of: " + final_roll, extra={"method": "GET", "status": 200, "level": "info"})

#     return final_roll

# def do_roll():
#     return randint(1, 6)

# driver function
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
    # logger_provider.shutdown()
