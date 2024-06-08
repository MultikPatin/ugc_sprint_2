from src.brokers.base import BaseBrokerProducer
from src.brokers.kafka import get_kafka_producer
from src.models.events import EM


class EventHandler:
    """Events user handler"""

    def __init__(self, producer: BaseBrokerProducer):
        self.producer = producer

    def send_message(self, topic: str, key: str, data: EM) -> None:
        """Sending message to broker producer."""
        self.producer.produce(
            topic=topic,
            context=data,
            key=key,
        )


def get_event_handler() -> EventHandler:
    return EventHandler(producer=get_kafka_producer())
