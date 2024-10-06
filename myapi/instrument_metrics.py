from prometheus_fastapi_instrumentator import Instrumentator

def MetricsInstrumentor(app, service_name='myproject'):
    Instrumentator(excluded_handlers=["/metrics"]).instrument(app).expose(app)

