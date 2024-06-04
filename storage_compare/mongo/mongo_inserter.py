import csv

from pymongo import MongoClient

from schemas import SCHEMAS_MAPPING
from service import MongoManager


def populate_collection(collection, filename, schema):
    items = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        for row in reader:
            data = SCHEMAS_MAPPING[schema].from_list(row)
            items.append(data.dict())

    manager.insert_data(collection, items)


if __name__ == '__main__':
    client = MongoClient("localhost", 27017)
    manager = MongoManager(client)
    populate_collection('reviews', 'reviews.csv', 'review')
    populate_collection('reviews_likes', 'reviews_rating.csv', 'review_like')
    populate_collection('movies_likes', 'movies_rating.csv', 'movie_like')
    populate_collection('bookmarks', 'bookmarks.csv', 'bookmark')
