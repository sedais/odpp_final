import json
from pymongo import MongoClient
from pymongo.server_api import ServerApi

from youtube_api import *
from web_scraper_ifixit import *


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


# def insert_to_mongodb(ifixit, youtube):
#     client = connect_to_mongo_db()
#     logging.info("Available databases in mongo db: ")
#     logging.info(client.list_database_names())
#     db = client.YouTubeDB
#     phone_collection = db.phones
#     youtube_collection = db.youtube
#
#     logging.info("Deleting the existing collections...")
#     phone_collection.delete_many({})
#     youtube_collection.delete_many({})
#     logging.info("Deleted collections.")
#
#     logging.info("Inserting ifixit and youtube data into collections...")
#     phone_collection.insert_many(ifixit)
#     youtube_collection.insert_many(youtube)
#     logging.info("Inserted.")

def insert_to_mongodb(youtube):
    client = connect_to_mongo_db()
    logging.info("Available databases in mongo db: ")
    logging.info(client.list_database_names())
    db = client.YouTubeDB
    youtube_collection = db.youtube

    logging.info("Deleting the existing collections...")
    youtube_collection.delete_many({})
    logging.info("Deleted collections.")

    logging.info("Inserting youtube data into collections...")
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
    df_ifixit = get_the_content()
    phone_names = df_ifixit["brand"] + " " + df_ifixit["model"]
    print(type(phone_names.values))
    print(list(phone_names))
    phone_names_list = list(phone_names)
    cols = ["phone_name", "video_id", "transcript_list"]
    print(phone_names)
    query = "change phone battery"
    df_transcripts = pd.DataFrame(columns=cols)
    df_col = pd.DataFrame(columns=cols)
    phone_names_test = ["Google Pixel 6", "iPhone 12 Pro", "Samsung Galaxy Note"]
    print(phone_names_test)
    phone_names_list.remove("Huawei Mate 40 Pro")
    phone_names_list.remove("Google Pixel 5")
    phone_names_list.remove("iPhone SE 2020")
    phone_names_list.remove("Samsung Galaxy Z Flip")
    phone_names_list.remove("Samsung Galaxy S20 Ultra")
    phone_names_list.remove("Motorola razr")


    first_ten = phone_names_list[0:20]

    for name in first_ten:
        a_query = query + " " + name
        print(a_query)
        df_one_row = get_transcripts(df_transcripts, a_query, name, "", "video", 1)
        print("i m here: df_one_row")
        print(df_one_row)
        #pd.concat([df_col, df_one], ignore_index=True)
        #df_col_all = df_col.append(df_one_row, ignore_index=True)
        df_col = pd.concat([df_col, df_one_row], ignore_index=True)
        print(df_one_row)

    print("end of for loop")
    print(df_col)
    # xs = df_col["transcript_list"]
    # t = " ".join(str(x) for x in xs
    # df_col["texts"] = {}
    # for index in df_col.index.values:
    #     texts = df_col.iloc[index]["transcript_list"]
    #    #xs = df_col["transcript_list"]
    #     t = " ".join(str(x) for x in texts)
    #     print(t)
    #     df_col.iloc[index]["texts"] = t

        # df['phone_name'] = name
        #df_transcripts.loc[:, 'phone_name'] = name
        # df_transcripts = df_transcripts + df


    #df_search_api = get_transcripts(df_transcripts, a_query, "", "video", 1)

    #dict_ifixit = df_ifixit.to_dict('records')
    dict_youtube = df_col.to_dict('records')

    # pprint(dict_ifixit)

    insert_to_mongodb(dict_youtube)
