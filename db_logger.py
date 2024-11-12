import datetime

from pymongo import MongoClient

MONGO_INITDB_ROOT_USERNAME = "evg"
MONGO_INITDB_ROOT_PASSWORD = "23a953fd599c"
MONGO_PATH = "localhost/"
MONGO_DB = "ai-youtube-subtitles"
REQUEST_LOG_DOCUMENT = "request_log"
MONGO_PORT = 27017

request_log_document = None


def get_mongo_document():
    global request_log_document

    if request_log_document is not None:
        return request_log_document

    try:
        connection_string = f"mongodb://{MONGO_INITDB_ROOT_USERNAME}:{MONGO_INITDB_ROOT_PASSWORD}@{MONGO_PATH}"
        mongo_client = MongoClient(connection_string, MONGO_PORT)
        database = mongo_client[MONGO_DB]
        request_log_document = database[REQUEST_LOG_DOCUMENT]
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        request_log_document = None

    return request_log_document


def db_write_request(url, request_params):
    doc = get_mongo_document()
    if doc is not None:
        log_entry = {
            "url": url,
            "request_params": request_params,
            "date_time": datetime.datetime.now(datetime.UTC)
        }
        doc.insert_one(log_entry)
