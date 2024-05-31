from dotenv import load_dotenv
from pydantic.fields import Field
from pydantic_settings import BaseSettings
from pydantic_settings.main import SettingsConfigDict

load_dotenv()


class ClickhouseSettings(BaseSettings):
    host: str = Field(alias="CH_HOST")
    username: str = Field(alias="CH_USERNAME")
    password: str = Field(alias="CH_PASSWORD")


class VerticaSettings(BaseSettings):
    host: str = Field(alias="VERTICA_HOST")
    user: str = Field(alias="VERTICA_USER")
    port: int = Field(alias="VERTICA_PORT", default=5433)
    database: str = Field(alias="VERTICA_DATABASE")
    password: str = Field(alias="VERTICA_PASSWORD", default="")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    clickhouse: ClickhouseSettings = ClickhouseSettings()
    vertica: VerticaSettings = VerticaSettings()


settings = Settings()
