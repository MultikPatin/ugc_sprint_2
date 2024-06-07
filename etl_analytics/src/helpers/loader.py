import backoff

from clickhouse_driver import Client
from clickhouse_driver import errors as ch_errors

from src.config import ClickHouseSettings


class ClickHouseBaseLoader:
    _client: Client

    def __init__(self, config: ClickHouseSettings):
        self.__config = config

    @backoff.on_exception(
        wait_gen=backoff.expo, exception=(ch_errors.NetworkError, EOFError)
    )
    def connect(self):
        self._client = Client(
            host=self.__config.host,
            user=self.__config.username,
            password=self.__config.password,
        )
        self._client.execute("SHOW DATABASES")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self._client:
            self._client.disconnect()
