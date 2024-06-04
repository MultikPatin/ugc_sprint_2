from pymongo import MongoClient

from service import MongoManager

if __name__ == '__main__':
    client = MongoClient("localhost", 27017)

    manager = MongoManager(client)
    manager.get_user_bookmarks("edb44b78-827f-4b42-9a68-0f22da96ee41")
    manager.get_movie_likes_count("62071570-76c8-4b17-b9c5-0fd495bd0781")
    manager.get_average_movies_rating()
    manager.get_likes_by_user("ccc37f0c-76a0-4d46-8e13-20594ee25254")
