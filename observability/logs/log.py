
import logging
import requests
from opentelemetry.trace import get_current_span
from .config import LogConfig
from .formatters import LokiFormatter

class OTELSpanFilter(logging.Filter):
    def filter(self, record):
        span = get_current_span()
        trace_id = ""
        span_id = ""
        if span and span.get_span_context().is_valid:
            ctx = span.get_span_context()
            trace_id = format(ctx.trace_id, "032x")
            span_id = format(ctx.span_id, "016x")
        # attach as logrecord extra, this is to print in logs
        record.trace_id = trace_id
        record.span_id = span_id
        return True

_config = LogConfig()
logger = logging.getLogger("observability")
logger.setLevel(_config.LOG_LEVEL)

handler = logging.StreamHandler()
handler.setFormatter(LokiFormatter('%(asctime)s %(levelname)s %(message)s trace_id=%(trace_id)s span_id=%(span_id)s'))

# injecting to logs using filter
handler.addFilter(OTELSpanFilter())
logger.addHandler(handler)

class LokiLogHandler(logging.Handler):
    def emit(self, record):
        # here dont need to catch span again
        log_entry = self.format(record)
        try:
            requests.post(
                _config.LOKI_URL,
                json={
                    "streams": [{
                        "stream": {"level": record.levelname.lower()},
                        "values": [[str(int(record.created*1e9)), log_entry]]
                    }]
                },
                timeout=0.5,
            )
        except Exception:
            pass  # silently ignoring but can be improved in prod #TODO

loki_handler = LokiLogHandler()
loki_handler.setFormatter(LokiFormatter('%(asctime)s %(levelname)s %(message)s trace_id=%(trace_id)s span_id=%(span_id)s'))
loki_handler.addFilter(OTELSpanFilter())  # apply filter to Loki handler as well
logger.addHandler(loki_handler)
