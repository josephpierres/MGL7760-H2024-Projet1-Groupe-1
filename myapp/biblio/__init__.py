import datetime
import logging
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_redis import FlaskRedis
from flask_wtf.csrf import CSRFProtect
from config import ProductionConfig



##########################
# OpenTelemetry Settings #
##########################
from biblio.instrument_logging import LogsInstrumentor
from biblio.instrument_tracing import TracesInstrumentor
from biblio.instrument_metrics import MetricsInstrumentor

service_name = "biblio_app"
otlp_endpoint = os.environ.get("OTLP_GRPC_ENDPOINT", "http://localhost:4317")
app = Flask(__name__)

# Instrument tracing
tracer = TracesInstrumentor(app=app, service_name=service_name, otlp_endpoint=otlp_endpoint, excluded_urls="/metrics")

# Instrument logging
handler = LogsInstrumentor(service_name=service_name, otlp_endpoint=otlp_endpoint)

# Attach OTLP handler to root logger
logger = logging.getLogger(__name__)

app.logger.addHandler(handler)
app.config.from_object(ProductionConfig)

# Initialize CSRF protection, database, and Redis
csrf = CSRFProtect(app)
db = SQLAlchemy(app)
redis_client = FlaskRedis(app)

# handler.setLevel(logging.DEBUG)

logger.setLevel(logging.INFO)

with app.app_context():
    # Instrument Flask, SQLAlchemy, and Redis with OpenTelemetry
    from opentelemetry.instrumentation.flask import FlaskInstrumentor
    from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
    from opentelemetry.instrumentation.redis import RedisInstrumentor
    from opentelemetry.instrumentation.requests import RequestsInstrumentor

    FlaskInstrumentor().instrument( enable_commenter=True, commenter_options={})
    FlaskInstrumentor().instrument_app(app)
    SQLAlchemyInstrumentor().instrument(
        engine=db.engine,
        tracer_provider=tracer,
        enable_commenter=True,
        commenter_options={},)
    RedisInstrumentor().instrument()
    RequestsInstrumentor().instrument()  
    MetricsInstrumentor(app=app, service_name=service_name) 
    
    # Check if the connection is successfully established or not

    try:
        db.session.execute(text('SELECT 1'))
        print('\n---****** Connexion à MySQL réussie ******')
    except Exception as e:
        print('\n----------- Connexion échouée ! ERROR : ', e)

# Routes and Models import
from . import routes, models
