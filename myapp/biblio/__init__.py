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

from opentelemetry.instrumentation.wsgi import collect_request_attributes
from opentelemetry.sdk.resources import Resource
from opentelemetry.propagate import extract

# Import exporters
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http._log_exporter import ( OTLPLogExporter,)


# Trace imports
from opentelemetry import trace
from opentelemetry.trace import ( 
    SpanKind, set_tracer_provider, get_tracer_provider
    )
from opentelemetry.sdk.trace import TracerProvider, sampling
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)

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
            "service.name": "biblio-mgmt",
            "service.instance.id": "biblio-mgmt",
        }
    )

# create the log providers ****

logger_provider = LoggerProvider(resource=resource)

# set the  providers

set_logger_provider(logger_provider)

log_exporter = OTLPLogExporter() 
    #endpoint=os.getenv("OTLP_ENDPOINT", "localhost:4317/v1/logs"), 
    # insecure=json.loads(os.getenv("INSECURE", "true").lower()))

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

trace_exporter = OTLPSpanExporter()
    # endpoint=os.getenv("OTLP_ENDPOINT", "http://otelcol:4317/v1/traces"), 
   # insecure=json.loads(os.getenv("INSECURE", "true").lower()), )

span = BatchSpanProcessor(trace_exporter)
tracer_provider.add_span_processor(span)

tracer = get_tracer_provider().get_tracer(__name__)

# get_tracer_provider().add_span_processor(
#     BatchSpanProcessor(ConsoleSpanExporter())
# )

# create the metric providers *****************

exporter = OTLPMetricExporter() 
    # endpoint=os.getenv("OTLP_ENDPOINT", "localhost:4318"), 
    #                           insecure=json.loads(os.getenv("INSECURE", "true").lower()),
    #                           preferred_temporality = {
    #                                 Counter: AggregationTemporality.DELTA,
    #                                 UpDownCounter: AggregationTemporality.CUMULATIVE,
    #                                 Histogram: AggregationTemporality.DELTA,
    #                                 ObservableCounter: AggregationTemporality.DELTA,
    #                                 ObservableUpDownCounter: AggregationTemporality.CUMULATIVE,
    #                             }
    #                         )
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




logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

meter = metrics.get_meter(__name__)






with app.app_context():
    # Instrument Flask, SQLAlchemy, and Redis with OpenTelemetry
    FlaskInstrumentor().instrument_app(app)
    SQLAlchemyInstrumentor().instrument(engine=db.engine)
    RedisInstrumentor().instrument()
    RequestsInstrumentor().instrument()     
    # Check if the connection is successfully established or not

    try:
        db.session.execute(text('SELECT 1'))
        print('\n---****** Connexion à MySQL réussie ******')
        logger.info("****** Connexion à MySQL réussie ******'")
    except Exception as e:
        print('\n----------- Connexion échouée ! ERROR : ', e)

# Routes and Models import
from . import routes, models

# @app.route("/server_request")
# def server_request():
#     with tracer.start_as_current_span(
#         "server_request",
#         context=extract(request.headers),
#         kind=SpanKind.SERVER,
#         attributes=collect_request_attributes(request.environ),
#     ):
#         print(request.args.get("param"))
#         return "served"

# @app.route('/')
# def index():
#     final_roll = str(do_roll())
#     args = request.args
#     user = args.get('user',  "anonymous")
#     logger.info("completed request for user: " + user + "with dice roll of: " + final_roll, extra={"method": "GET", "status": 200, "level": "info"})

#     return final_roll

# def do_roll():
#     return randint(1, 6)

# driver function
if __name__ == '__main__':
    app.run(host='0.0.0.0')
    # logger_provider.shutdown()
