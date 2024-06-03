from kafka import KafkaProducer

from src.brokers.base import BaseBrokerProducer
from src.core.config import settings
from src.models.events import EventModel


class KafkaBrokerProducer(BaseBrokerProducer):
    """Kafka producer for sending messages to kafka topic"""

    def __init__(self, producer: KafkaProducer):
        self.producer = producer

    def produce(self, topic: str, key: str, context: EventModel) -> None:
        """Sending message to kafka topic"""
        self.producer.send(
            topic=topic,
            value=context.model_dump_json().encode("utf-8"),
            key=bytes(key, "UTF-8"),
        )


def get_kafka_producer() -> BaseBrokerProducer:
    return KafkaBrokerProducer(producer=KafkaProducer(bootstrap_servers=[settings.kafka.bootstrap_servers]))
