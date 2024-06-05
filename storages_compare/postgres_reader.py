import csv
from typing import List

from service import PGManager
from utils import conn_context_postgres, get_postgres_dsl


def generate_data(filename: str, with_id=False) -> List[List]:
    items = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        for idx, row in enumerate(reader, start=1):
            if with_id:
                row.insert(0, idx)  # type: ignore
            items.append(row)
    return items


if __name__ == "__main__":
    dsl: dict = get_postgres_dsl()
    with conn_context_postgres(dsl) as pg_conn: # type: ignore
        manager = PGManager(pg_conn)
        manager.get_user_bookmarks("edb44b78-827f-4b42-9a68-0f22da96ee41")
        manager.get_movie_likes_count("62071570-76c8-4b17-b9c5-0fd495bd0781")
        manager.get_average_movies_rating()
        manager.get_likes_by_user("ccc37f0c-76a0-4d46-8e13-20594ee25254")

