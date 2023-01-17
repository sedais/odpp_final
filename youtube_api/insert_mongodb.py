import json
from pymongo import MongoClient
from pymongo.server_api import ServerApi

from api_search import *
from ifixit.web_scraper_ifixit import *


def test():
    try:
        logging.info("Test connection to MongoDB Cloud is being established...")
        client = MongoClient(
            "mongodb+srv://sedaismail:1234@cluster0.65tresj.mongodb.net/?retryWrites=true&w=majority",
            server_api=ServerApi('1'))
        logging.info("Available databases in mongo db: ")
        logging.info(client.list_database_names())
        db = client.YouTubeDB
        collection = db.phones
        print(collection)

    except Exception as e:
        logging.error(e)
    else:
        logging.info("Test connection is successful")


def connect_to_mongo_db():
    client = MongoClient(
        "mongodb+srv://sedaismail:1234@cluster0.65tresj.mongodb.net/?retryWrites=true&w=majority",
        server_api=ServerApi('1'))
    return client


def insert_to_mongodb(ifixit, youtube):
    client = connect_to_mongo_db()
    logging.info("Available databases in mongo db: ")
    logging.info(client.list_database_names())
    db = client.YouTubeDB
    phone_collection = db.phones
    youtube_collection = db.youtube

    logging.info("Deleting the existing collections...")
    phone_collection.delete_many({})
    youtube_collection.delete_many({})
    logging.info("Deleted collections.")

    logging.info("Inserting ifixit and youtube data into collections...")
    phone_collection.insert_many(ifixit)
    youtube_collection.insert_many(youtube)
    logging.info("Inserted.")


def insert_devices():
    client = connect_to_mongo_db()
    with open('devices.json') as file:
        file_data = json.load(file)
    db = client.PhoneDB
    collection = db.phones
    collection.insert_many(file_data["RECORDS"])
    client.close()


if __name__ == '__main__':
    # test()

    # insert devices to phoneDB
    # insert_devices()

    df_ifixit = get_the_content()
    query = "change phone battery"
    df_search_api = search_by_query(query, "video")

    dict_ifixit = df_ifixit.to_dict('records')
    dict_youtube = df_search_api.to_dict('records')

    # pprint(dict_ifixit)

    insert_to_mongodb(dict_ifixit, dict_youtube)
