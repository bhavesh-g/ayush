from pydantic_settings import BaseSettings, SettingsConfigDict

class TracingConfig(BaseSettings):
    OTEL_EXPORTER_OTLP_ENDPOINT: str
    OTEL_EXPORTER_TYPE: str = "console"
    OTEL_SERVICE_NAME: str = "ayush-obs-boilerplate"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
