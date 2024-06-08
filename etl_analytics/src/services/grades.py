import json
from typing import Generator, Any

from src.models.grades import GradeMessage
from src.helpers.extractor import KafkaBaseExtractor
from src.helpers.loader import ClickHouseBaseLoader


class KafkaExtractor(KafkaBaseExtractor):
    def get_data(self) -> Generator[GradeMessage, Any, None]:
        for message in self._consumer:
            mes = message.value.decode("utf-8").replace("'", '"')
            data = json.loads(mes)
            user_id = data.get("user_id")
            film_id = data.get("film_id")
            rating = data.get("rating")
            timestamp = data.get("timestamp")
            yield GradeMessage(
                user_id=user_id,
                film_id=film_id,
                rating=rating,
                timestamp=timestamp,
            )


class ClickHouseLoader(ClickHouseBaseLoader):
    def write_data(self, messages: list[GradeMessage]):
        self.connect()
        query = (
            "INSERT INTO default.grades (user_id, film_id, rating, timestamp) VALUES"
        )
        params = (
            (
                message.user_id,
                message.film_id,
                message.rating,
                message.timestamp,
            )
            for message in messages
        )
        self._client.execute(query=query, params=params)
