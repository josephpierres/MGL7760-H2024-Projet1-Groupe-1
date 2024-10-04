from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.wsgi import OpenTelemetryMiddleware
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource


def TracesInstrumentor(app, service_name, otlp_endpoint="http://localhost:4317", excluded_urls=""):
    resource = Resource.create(attributes={"service.name": service_name})
    tracer = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer)

    # trace_processor = BatchSpanProcessor(ConsoleSpanExporter())
    trace_processor = BatchSpanProcessor(
        OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)
    )
    tracer.add_span_processor(trace_processor)

    # instrument
    FlaskInstrumentor.instrument_app(
        app, tracer_provider=tracer, excluded_urls=excluded_urls
    )
    # c'etait pas la avant
    app.wsgi_app = OpenTelemetryMiddleware(app.wsgi_app)
    return tracer