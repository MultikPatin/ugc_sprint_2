import json

import backoff
from kafka import KafkaConsumer
from kafka import errors as kafka_errors

from src.etl_analytics.config import KafkaSettings
from src.etl_analytics.models.events import EventMessage


class KafkaExtractor:
    def __init__(self, config: KafkaSettings):
        self.consumer = None
        self.__config = config
        self.connect()

    @backoff.on_exception(
        wait_gen=backoff.expo, exception=kafka_errors.NoBrokersAvailable
    )
    def connect(self):
        self.consumer = KafkaConsumer(
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
        if self.consumer:
            self.consumer.close()

    def get_data(self) -> list[EventMessage]:
        for message in self.consumer:
            mes = message.value.decode("utf-8").replace("'", '"')
            data = json.loads(mes)
            service = data.get("service")
            user = data.get("user")
            timestamp = data.get("timestamp")
            entity_type = data.get("entity_type")
            entity = data.get("entity")
            action = data.get("action")
            yield EventMessage(
                service=service,
                user=user,
                timestamp=timestamp,
                entity_type=entity_type,
                entity=entity,
                action=action,
            )

    def commit(self):
        self.consumer.commit()
