from datetime import time
from flask import Flask, jsonify, request
from prometheus_client import make_wsgi_app, Counter, Histogram
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from opentelemetry.sdk.resources import Resource

def MetricsInstrumentor(app, service_name):
    resource = Resource.create(attributes={"service.name": service_name})
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
        '/metrics': make_wsgi_app()
    })


# REQUEST_COUNT = Counter(
#     'app_request_count',
#     'Application Request Count',
#     ['method', 'endpoint', 'http_status']
# )
# REQUEST_LATENCY = Histogram(
#     'app_request_latency_seconds',
#     'Application Request Latency',
#     ['method', 'endpoint']
# )
# @app.route('/')
# def hello():
#     start_time = time.time()
#     REQUEST_COUNT.labels('GET', '/', 200).inc()
#     response = jsonify(message='Hello, world!')
#     REQUEST_LATENCY.labels('GET', '/').observe(time.time() - start_time)
#     return response