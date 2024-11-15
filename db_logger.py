import datetime

from pymongo import MongoClient

MONGO_INITDB_ROOT_USERNAME = "evg"
MONGO_INITDB_ROOT_PASSWORD = "23a953fd599c"
MONGO_PATH = "localhost/"
MONGO_DB = "ai-youtube-subtitles"
REQUEST_LOG_DOCUMENT = "request_log"
MONGO_PORT = 27017

connection_string = f"mongodb://{MONGO_INITDB_ROOT_USERNAME}:{MONGO_INITDB_ROOT_PASSWORD}@{MONGO_PATH}"
mongo_client = MongoClient(connection_string,
                           MONGO_PORT,
                           connectTimeoutMS=3000,
                           socketTimeoutMS=3000,
                           serverSelectionTimeoutMS=3000)


def db_write_request(url, request_params):
    try:
        database = mongo_client[MONGO_DB]
        doc = database[REQUEST_LOG_DOCUMENT]
        if doc is not None:
            log_entry = {
                "url": url,
                "request_params": request_params,
                "date_time": datetime.datetime.now(datetime.UTC)
            }
            doc.insert_one(log_entry)
    except Exception as e:
        print(f"Error accessing MongoDB: {e}")
        return None
