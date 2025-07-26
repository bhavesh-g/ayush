from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from functools import wraps
from .config import TracingConfig
from .exporters import get_tracer_exporter

_cfg = TracingConfig()
resource = Resource.create({"service.name": _cfg.OTEL_SERVICE_NAME}) # can add more here like in base image env
provider = TracerProvider(resource=resource)
provider.add_span_processor(get_tracer_exporter())
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

def instrument(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with tracer.start_as_current_span(func.__name__):
            return func(*args, **kwargs)
    return wrapper

__all__ = ["instrument", "tracer"]
