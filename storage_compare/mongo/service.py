from pymongo.mongo_client import MongoClient

from utils import timeit


class MongoManager:
    def __init__(self, client: MongoClient) -> None:
        self.client = client
        self.db = self.client.ugc_db
        self.reviews = self.db.reviews
        self.reviews_likes = self.db.reviews_likes
        self.movies_likes = self.db.movies_likes
        self.bookmarks = self.db.bookmarks
        self.collection_mapping = {
            "reviews": self.reviews,
            "reviews_likes": self.reviews_likes,
            "movies_likes": self.movies_likes,
            "bookmarks": self.bookmarks
        }

    @timeit
    def insert_data(self, collection: str, data):
        """
        Метод добавления bulk данных в коллекцию
        """
        self.collection_mapping[collection].insert_many(data)

    @timeit
    def get_user_bookmarks(self, user_id: str) -> list:
        """
        Метод получения списка закладок пользователя
        """

        result = self.bookmarks.find({
            "user": user_id
        })
        return [r for r in result]

    @timeit
    def get_movie_likes_count(self, movie_id: str, rating: int = 10) -> list:
        """
        Метод получения количества лайков или дизлайков (10 - лайки, 0 - дизлайки) у фильма
        """
        result = self.movies_likes.aggregate([
            {
                "$match": {"movie": movie_id, "rating": rating}
            },
            {
                "$count": "Likes"
            }

        ]
        )
        return [r for r in result]

    @timeit
    def get_average_movies_rating(self) -> list:
        """
        Метод получения средней оценки по фильмам
        """
        result = self.movies_likes.aggregate([
            {"$group":
                 {"_id": "$movie",
                  "Average_Rating": {"$avg": "$rating"}}
             }
        ]
        )
        return [r for r in result]

    @timeit
    def get_likes_by_user(self, user_id: str) -> list:
        """
        Метод для запроса списка фильмов, которые понравились пользователю
        """
        result = self.movies_likes.find(
            {"user": user_id, "rating": 10}

        )
        return [r for r in result]
