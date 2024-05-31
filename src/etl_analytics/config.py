from dotenv import load_dotenv
from pydantic.fields import Field
from pydantic_settings import BaseSettings
from pydantic_settings.main import SettingsConfigDict

load_dotenv()


class KafkaSettings(BaseSettings):
    host: str = Field(..., alias="KAFKA_HOST")
    port: int = Field(..., alias="KAFKA_PORT")
    topic: str = Field(..., alias="KAFKA_TOPIC_NAME_1")
    batch_size: int = Field(..., alias="ETL_ANALYTICS_BATCH_SIZE")
    consumer_timeout: int = Field(..., alias="ETL_ANALYTICS_CONSUMER_TIMEOUT")
    auto_offset_reset: str = "earliest"
    group_id: str = "echo-messages-to-stdout"
    enable_auto_commit: bool = False


class ClickHouseSettings(BaseSettings):
    host: str = Field("clickhouse-node1", alias="CLICKHOUSE_HOST")
    username: str = Field("clickhouse-node1", alias="CLICKHOUSE_USERNAME")
    password: str = Field("clickhouse-node1", alias="CLICKHOUSE_PASSWORD")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    kafka: KafkaSettings = KafkaSettings()
    clickHouse: ClickHouseSettings = ClickHouseSettings()
    sleep_time: int = Field(..., alias="ETL_ANALYTICS_SLEEP_TIME")


settings = Settings()
