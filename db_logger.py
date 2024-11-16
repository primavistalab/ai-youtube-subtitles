import datetime

from flask import Request
from pymongo import MongoClient

MONGO_INITDB_ROOT_USERNAME = "evg"
MONGO_INITDB_ROOT_PASSWORD = "23a953fd599c"
MONGO_PATH = "localhost/"
MONGO_DB = "ai-youtube-subtitles"
LOG_COLLECTION = "request_log"
MONGO_PORT = 27017

connection_string = f"mongodb://{MONGO_INITDB_ROOT_USERNAME}:{MONGO_INITDB_ROOT_PASSWORD}@{MONGO_PATH}"
mongo_client = MongoClient(connection_string,
                           MONGO_PORT,
                           connectTimeoutMS=3000,
                           socketTimeoutMS=3000,
                           serverSelectionTimeoutMS=3000)


def get_collection():
    database = mongo_client[MONGO_DB]
    return database[LOG_COLLECTION]


def create_index(index_name: str, fields: list, unique: bool = False):
    collection = get_collection()
    indexes = collection.list_indexes()
    for index in indexes:
        if index.get("name") == index_name:
            return
    collection.create_index(fields, name=index_name, unique=unique)
    print(f"Index {index_name} created")


def db_write_request(request: Request):
    try:
        collection = get_collection()
        if collection is not None:
            log_entry = {
                "method": request.method,
                "url": request.path,
                "args": request.args,
                "date_time": datetime.datetime.now(datetime.UTC)
            }
            collection.insert_one(log_entry)
    except Exception as e:
        print(f"Error accessing MongoDB: {e}")
        return None


create_index(index_name="date_time_idx", fields=[("date_time", 1)], unique=False)
