import json
from typing import Generator, Any

from src.models.favorites import FavoriteMessage
from src.helpers.extractor import KafkaBaseExtractor
from src.helpers.loader import ClickHouseBaseLoader


class KafkaExtractor(KafkaBaseExtractor):
    def get_data(self) -> Generator[FavoriteMessage, Any, None]:
        for message in self._consumer:
            mes = message.value.decode("utf-8").replace("'", '"')
            data = json.loads(mes)
            user_id = data.get("user_id")
            film_id = data.get("film_id")
            timestamp = data.get("timestamp")
            yield FavoriteMessage(
                user_id=user_id,
                film_id=film_id,
                timestamp=timestamp,
            )


class ClickHouseLoader(ClickHouseBaseLoader):
    def write_data(self, messages: list[FavoriteMessage]):
        self.connect()
        query = "INSERT INTO default.favorites (user_id, film_id, timestamp) VALUES"
        params = (
            (
                message.user_id,
                message.film_id,
                message.timestamp,
            )
            for message in messages
        )
        self._client.execute(query=query, params=params)
