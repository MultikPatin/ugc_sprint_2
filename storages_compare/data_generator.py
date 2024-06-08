import csv
import random
from uuid import uuid4, UUID
from typing import List

from faker import Faker

faker = Faker()

# Генерируем пул uuid для пользователей

users = [uuid4() for _ in range(100)]

# Генерируем пул uuid для фильмов

movies = [uuid4() for _ in range(1000)]

# Генерируем пул uuid для фильмов

reviews: List[UUID] = []


def generate_reviews() -> None:
    with open('reviews.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        for _ in range(1_000_000):
            uuid = uuid4()
            global reviews
            reviews.append(uuid)
            review = [
                str(random.choice(reviews)),
                faker.name(),
                faker.text(),
                str(faker.date_time_this_year()),
                str(random.choice(users)),
                str(random.choice(movies))
            ]
            writer.writerow(review)


def generate_reviews_rating() -> None:
    with open('reviews_rating.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        for _ in range(1_000_000):
            review_rating = [
                str(random.choice(reviews)),
                random.randint(1, 10),
                str(random.choice(users)),
            ]
            writer.writerow(review_rating)


def generate_movies_rating() -> None:
    with open('movies_rating.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        for _ in range(1_000_000):
            movie_rating = [
                str(random.choice(movies)),
                random.randint(1, 10),
                str(random.choice(users)),
            ]
            writer.writerow(movie_rating)


def generate_generate_bookmarks() -> None:
    with open('bookmarks.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        for _ in range(len(users)):
            bookmarks = [
                str(users.pop()),
                ",".join([str(random.choice(movies)) for _ in range(0, random.randint(1, 20))])
            ]
            writer.writerow(bookmarks)


if __name__ == '__main__':
    generate_reviews()
    generate_reviews_rating()
    generate_movies_rating()
    generate_generate_bookmarks()
