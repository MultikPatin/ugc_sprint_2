import json
from typing import Generator, Any

from src.models.reviews import ReviewMessage
from src.helpers.extractor import KafkaBaseExtractor
from src.helpers.loader import ClickHouseBaseLoader


class KafkaExtractor(KafkaBaseExtractor):
    def get_data(self) -> Generator[ReviewMessage, Any, None]:
        for message in self._consumer:
            mes = message.value.decode("utf-8").replace("'", '"')
            data = json.loads(mes)
            id = data.get("id")
            film_id = data.get("film_id")
            author = data.get("author")
            text = data.get("text")
            rating = data.get("rating")
            timestamp = data.get("timestamp")
            yield ReviewMessage(
                id=id,
                film_id=film_id,
                author=author,
                text=text,
                rating=rating,
                timestamp=timestamp,
            )


class ClickHouseLoader(ClickHouseBaseLoader):
    def write_data(self, messages: list[ReviewMessage]):
        self.connect()
        query = "INSERT INTO default.reviews (id, film_id, author, text, rating, timestamp) VALUES"
        params = (
            (
                message.id,
                message.film_id,
                message.author,
                message.text,
                message.rating,
                message.timestamp,
            )
            for message in messages
        )
        self._client.execute(query=query, params=params)
