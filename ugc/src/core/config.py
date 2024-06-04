import os

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PREFIX_BASE_ROUTE = "/api/v1"


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


class AppSettings(EnvSettings):
    debug: bool = Field(default=False)


class SentrySettings(EnvSettings):
    dsn: str = Field(..., alias="SENTRY_DSN")


class LogstashSettings(EnvSettings):
    host: str = Field(..., alias="LOGSTASH_HOST")
    port: int = Field(..., alias="LOGSTASH_PORT")


class SwaggerSettings(EnvSettings):
    project_name: str = Field(default="UGC Service")
    docs_url: str = "/api/openapi"
    api_url: str = "/static/api/v1/openapi.yaml"
    openapi_url: str = "/api/openapi.json"
    version: str = "0.1.0"


class KafkaSettings(EnvSettings):
    kafka_host: str = Field(default="localhost")
    kafka_port: int = Field(default=9094)

    @computed_field
    def bootstrap_servers(self) -> str:
        return f"{self.kafka_host}:{self.kafka_port}"


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    sentry: SentrySettings = SentrySettings()
    logstash: LogstashSettings = LogstashSettings()
    swagger: SwaggerSettings = SwaggerSettings()
    kafka: KafkaSettings = KafkaSettings()


settings = Settings()
