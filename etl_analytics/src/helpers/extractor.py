import backoff
from kafka import KafkaConsumer
from kafka import errors as kafka_errors

from src.config import KafkaSettings


class KafkaBaseExtractor:
    _consumer: KafkaConsumer

    def __init__(self, config: KafkaSettings):
        self.__config = config
        self.connect()

    @backoff.on_exception(
        wait_gen=backoff.expo, exception=kafka_errors.NoBrokersAvailable
    )
    def connect(self):
        self._consumer = KafkaConsumer(
            self.__config.topic,
            bootstrap_servers=[f"{self.__config.host}:{self.__config.port}"],
            auto_offset_reset=self.__config.auto_offset_reset,
            enable_auto_commit=self.__config.enable_auto_commit,
            group_id=self.__config.group_id,
            consumer_timeout_ms=self.__config.consumer_timeout * 1000,
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self._consumer:
            self._consumer.close()

    def commit(self):
        self._consumer.commit()
