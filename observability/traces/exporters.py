from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from .config import TracingConfig

def get_tracer_exporter():
    cfg = TracingConfig()
    if cfg.OTEL_EXPORTER_TYPE.lower() == "otlp":
        exporter = OTLPSpanExporter(endpoint=cfg.OTEL_EXPORTER_OTLP_ENDPOINT)
    else:
        exporter = ConsoleSpanExporter()
    return BatchSpanProcessor(exporter)
