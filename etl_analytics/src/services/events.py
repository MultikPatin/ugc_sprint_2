import json
from typing import Generator, Any

from src.models.events import EventMessage
from src.helpers.extractor import KafkaBaseExtractor
from src.helpers.loader import ClickHouseBaseLoader


class KafkaExtractor(KafkaBaseExtractor):
    def get_data(self) -> Generator[EventMessage, Any, None]:
        for message in self._consumer:
            mes = message.value.decode("utf-8").replace("'", '"')
            data = json.loads(mes)
            service = data.get("service")
            user_id = data.get("user")
            timestamp = data.get("timestamp")
            entity_type = data.get("entity_type")
            entity = data.get("entity")
            action = data.get("action")
            yield EventMessage(
                service=service,
                user_id=user_id,
                timestamp=timestamp,
                entity_type=entity_type,
                entity=entity,
                action=action,
            )


class ClickHouseLoader(ClickHouseBaseLoader):
    def write_data(self, messages: list[EventMessage]):
        self.connect()
        query = "INSERT INTO default.events (service, user_id, timestamp, entity_type, entity, action) VALUES"
        params = (
            (
                message.service,
                message.user_id,
                message.timestamp,
                message.entity_type,
                message.entity,
                message.action,
            )
            for message in messages
        )
        self._client.execute(query=query, params=params)
