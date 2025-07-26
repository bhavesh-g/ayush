from pydantic_settings import BaseSettings, SettingsConfigDict

class LogConfig(BaseSettings):
    LOG_LEVEL: str = "INFO"
    LOKI_URL: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
