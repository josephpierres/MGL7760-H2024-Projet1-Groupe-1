
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource

import logging
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry import _logs
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor


def LogsInstrumentor(service_name, otlp_endpoint="http://localhost:4317"):
    resource = Resource.create(attributes={"service.name": service_name})
    logger_provider = LoggerProvider(resource=resource)
    _logs.set_logger_provider(logger_provider)
    log_processor = BatchLogRecordProcessor(
        OTLPLogExporter(endpoint=otlp_endpoint, insecure=True)
    )
    logger_provider.add_log_record_processor(log_processor)

    # Attach OTLP handler to logger
    handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)

    class EndpointFilter(logging.Filter):
        # Uvicorn endpoint access log filter
        def filter(self, record: logging.LogRecord) -> bool:
            return record.getMessage().find("GET /metrics") == -1

    # Filter out /metrics
    logging.getLogger("uvicorn.access").addFilter(EndpointFilter())

    # instrument
    LoggingInstrumentor().instrument(set_logging_format=True)

    return handler