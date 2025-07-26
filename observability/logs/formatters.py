import logging

class LokiFormatter(logging.Formatter):
    def format(self, record):
        trace_id = getattr(record, "trace_id", "")
        span_id = getattr(record, "span_id", "")
        base = super().format(record)
        extras = f" trace_id={trace_id} span_id={span_id}" if trace_id or span_id else ""
        return f"{base}{extras}"
