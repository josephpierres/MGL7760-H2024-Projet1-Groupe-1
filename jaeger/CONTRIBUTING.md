You can then navigate to http://localhost:16686 to access the Jaeger UI.

You can configure the exporter with the following environment variables:

OTEL_EXPORTER_JAEGER_USER

OTEL_EXPORTER_JAEGER_PASSWORD

OTEL_EXPORTER_JAEGER_ENDPOINT

OTEL_EXPORTER_JAEGER_AGENT_PORT

OTEL_EXPORTER_JAEGER_AGENT_HOST

OTEL_EXPORTER_JAEGER_AGENT_SPLIT_OVERSIZED_BATCHES

OTEL_EXPORTER_JAEGER_TIMEOUT

- JAEGER_REPORTER_LOG_SPANS=true
- JAEGER_SAMPLER_PARAM=1
- JAEGER_SAMPLER_TYPE=const


5775	UDP	agent	accept zipkin.thrift over compact thrift protocol (deprecated, used by legacy clients only)
6831	UDP	agent	accept jaeger.thrift over compact thrift protocol
6832	UDP	agent	accept jaeger.thrift over binary thrift protocol
5778	HTTP	agent	serve configs
16686	HTTP	query	serve frontend
14268	HTTP	collector	accept jaeger.thrift directly from clients
14250	HTTP	collector	accept model.proto
9411	HTTP	collector	Zipkin compatible endpoint (optional)


