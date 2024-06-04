from typing import List

from psycopg2.extensions import connection as _connection
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


class PGManager:
    def __init__(self, connection: _connection) -> None:
        self.connection = connection

    def create_initial_tables(self) -> None:
        with self.connection.cursor() as cursor:
            reviews: str = """
            CREATE TABLE IF NOT EXISTS reviews (id uuid PRIMARY KEY, title varchar(255), body TEXT, created_at 
            timestamp, author UUID, movie UUID)
            """
            cursor.execute(reviews)
            reviews_likes: str = """
            CREATE TABLE IF NOT EXISTS reviews_likes (id serial PRIMARY KEY, review uuid, rating smallint, user_id uuid)
            """
            cursor.execute(reviews_likes)
            movies_likes: str = """
            CREATE TABLE IF NOT EXISTS movies_likes (id serial PRIMARY KEY, movie uuid, rating smallint, user_id uuid)
            """
            cursor.execute(movies_likes)
            bookmarks: str = """
            CREATE TABLE IF NOT EXISTS bookmarks (id serial PRIMARY KEY,  user_id uuid, movies varchar[])
            """
            cursor.execute(bookmarks)
            self.connection.commit()

    @timeit
    def insert_data(self, data: List[list], table_name: str, col_count: int):
        """
        Метод для вставки данных
        """
        col_placeholders: str = ', '.join(['%s'] * col_count)
        with self.connection.cursor() as cursor:
            args_str = ','.join(cursor.mogrify(f"({col_placeholders})", i).decode('utf-8')
                                for i in data)
            cursor.execute(f"INSERT INTO {table_name} VALUES " + args_str + " ON CONFLICT DO NOTHING")
            self.connection.commit()

    @timeit
    def insert_bookmarks(self, data: List[list]):
        """
        Метод для вставки закладок пользователя
        """
        with self.connection.cursor() as cursor:
            for row in data:
                row[2] = row[2].split(',')
                query = f"""INSERT INTO bookmarks (id, user_id, movies) VALUES ({row[0]}, '{row[1]}', ARRAY{row[2]})"""
                cursor.execute(query)
                self.connection.commit()
