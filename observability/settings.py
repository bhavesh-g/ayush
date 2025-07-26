from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
    LOG_LEVEL: str = "INFO"
    LOKI_URL: str
    OTEL_EXPORTER_OTLP_ENDPOINT: str
    OTEL_EXPORTER_TYPE: str = "console"
    OTEL_SERVICE_NAME: str = "ayush-obs-boilerplate"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = AppSettings()
