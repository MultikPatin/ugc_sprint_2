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
        manager.create_initial_tables()
        reviews = generate_data('reviews.csv')
        manager.insert_data(reviews, 'reviews', 6)
        reviews_likes = generate_data('reviews_rating.csv', with_id=True)
        manager.insert_data(reviews_likes, 'reviews_likes')
        movies_likes = generate_data('movies_rating.csv', with_id=True)
        manager.insert_data(movies_likes, 'movies_likes', 4)
        bookmarks = generate_data('bookmarks.csv', with_id=True)
        manager.insert_bookmarks(bookmarks)
