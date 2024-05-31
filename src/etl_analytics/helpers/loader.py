import backoff
from clickhouse_driver import Client
from clickhouse_driver import errors as ch_errors

from src.etl_analytics.config import ClickHouseSettings
from src.etl_analytics.models.events import EventMessage


class ClickHouseLoader:
    def __init__(self, config: ClickHouseSettings):
        self.__config = config
        self.client = None

    @backoff.on_exception(
        wait_gen=backoff.expo, exception=(ch_errors.NetworkError, EOFError)
    )
    def connect(self):
        self.client = Client(
            host=self.__config.host,
            user=self.__config.username,
            password=self.__config.password,
        )
        self.client.execute("SHOW DATABASES")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.client:
            self.client.disconnect()

    def write_data(self, messages: list[EventMessage]):
        self.connect()
        self.client.execute(
            "INSERT INTO default.events (service, user, timestamp, entity_type, entity, action) VALUES",
            (
                (
                    message.service,
                    message.user,
                    message.timestamp,
                    message.entity_type,
                    message.entity,
                    message.action,
                )
                for message in messages
            ),
        )
