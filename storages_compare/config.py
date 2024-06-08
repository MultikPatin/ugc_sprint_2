from dotenv import load_dotenv
from pydantic.fields import Field
from pydantic_settings import BaseSettings
from pydantic_settings.main import SettingsConfigDict

load_dotenv()


class MongoSettings(BaseSettings):
    host: str = Field(alias="MONGO_HOST", default="localhost")
    port: int = Field(alias="MONGO_PORT", default=27017)


class PGSettings(BaseSettings):
    host: str = Field(alias="POSTGRES_HOST", default="localhost")
    port: int = Field(alias="POSTGRES_PORT", default=5432)
    username: str = Field(alias="POSTGRES_USER")
    password: str = Field(alias="POSTGRES_PASSWORD")
    db: str = Field(alias="POSTGRES_DB")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="..env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    mongo: MongoSettings = MongoSettings()
    postgres: PGSettings = PGSettings()  # type: ignore


settings = Settings()
