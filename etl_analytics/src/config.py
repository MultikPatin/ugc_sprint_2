import os

from pydantic.fields import Field
from pydantic_settings import BaseSettings
from pydantic_settings.main import SettingsConfigDict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


class KafkaSettings(EnvSettings):
    host: str = Field(..., alias="KAFKA_HOST")
    port: int = Field(..., alias="KAFKA_PORT")
    topic: str = Field(..., alias="KAFKA_TOPIC")
    batch_size: int = Field(..., alias="ETL_ANALYTICS_BATCH_SIZE")
    consumer_timeout: int = Field(..., alias="ETL_ANALYTICS_CONSUMER_TIMEOUT")
    auto_offset_reset: str = "earliest"
    group_id: str = "echo-messages-to-stdout"
    enable_auto_commit: bool = False


class ClickHouseSettings(EnvSettings):
    host: str = Field(..., alias="CLICKHOUSE_HOST")
    username: str = Field(..., alias="CLICKHOUSE_USERNAME")
    password: str = Field(..., alias="CLICKHOUSE_PASSWORD")


class AppSettings(EnvSettings):
    sleep_time: int = Field(..., alias="ETL_ANALYTICS_SLEEP_TIME")


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    kafka: KafkaSettings = KafkaSettings()
    clickHouse: ClickHouseSettings = ClickHouseSettings()


settings = Settings()
