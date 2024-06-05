import logging
from typing import Any

from kafka.admin import KafkaAdminClient, NewTopic

from src.core.config import settings

TOPIC_LIST: list[str] = ["events"]

topic_config: dict[str, Any] = {
    "num_partitions": 3,
    "replication_factor": 3,
    "topic_configs": {
        "retention.ms": 86400000,
        "min.insync.replicas": 2,
        "cleanup.policy": "delete",
    },
}


class KafkaInit:
    def __init__(self):
        self.topics_list = []
        self.admin_client = KafkaAdminClient(
            bootstrap_servers=f"{settings.kafka.kafka_host}:{settings.kafka.kafka_port}",
            client_id="test",
        )

    def append_topic(self, name: str, config: dict[str, Any]):
        if name not in self.admin_client.list_topics():
            self.topics_list.append(NewTopic(name=name, **config))

    def create_topics(self):
        for topic_name in TOPIC_LIST:
            try:
                self.append_topic(name=topic_name, config=topic_config)
                logging.info(f"Topic {topic_name} appended")
            except Exception:
                logging.error(f"Topic {topic_name} didn't append")

        try:
            self.admin_client.create_topics(new_topics=self.topics_list, validate_only=False)
            logging.info("All topics created")
        except NotImplementedError:
            logging.error("Topics didn't create")


def get_kafka_init() -> KafkaInit:
    return KafkaInit()
