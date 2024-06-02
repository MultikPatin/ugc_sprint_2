import backoff

from clickhouse_driver import Client
from clickhouse_driver import errors as ch_errors

from config import ClickHouseSettings
from models.events import EventMessage


class ClickHouseLoader:
    __client: Client

    def __init__(self, config: ClickHouseSettings):
        self.__config = config

    @backoff.on_exception(
        wait_gen=backoff.expo, exception=(ch_errors.NetworkError, EOFError)
    )
    def connect(self):
        self.__client = Client(
            host=self.__config.host,
            user=self.__config.username,
            password=self.__config.password,
        )
        self.__client.execute("SHOW DATABASES")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.__client:
            self.__client.disconnect()

    def write_data(self, messages: list[EventMessage]):
        self.connect()
        query = "INSERT INTO default.events (service, user, timestamp, entity_type, entity, action) VALUES"
        params = (
            (
                message.service,
                message.user,
                message.timestamp,
                message.entity_type,
                message.entity,
                message.action,
            )
            for message in messages
        )
        self.__client.execute(query=query, params=params)
