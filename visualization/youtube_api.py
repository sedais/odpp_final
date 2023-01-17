import requests
import logging
import pandas as pd
import torch
import sys
import os
from youtube_transcript_api import YouTubeTranscriptApi
from web_scraper_ifixit import get_content_from_mongo
from tabulate import tabulate
from pymongo import MongoClient
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline



# API Keys
# api_key = "AIzaSyBSuf1z7mqV9-2IH5WbIJzkrsM5b2KHBMU"
# api_key = "AIzaSyD5_DJ3nv9CySefqkEZH3jVEzzzewuwKbw"
# api_key = "AIzaSyDwBns_kxeusJEy1iU1L5aDbQ0GvbCA2tg"
# api_key = "AIzaSyAwBN7ZnVlzHTiG9e3s7XyFOdXefcDYKnk"
# api_key = "AIzaSyCMhPvzt2_lAOAsypiBCVJ2_uEivENlTIo"
# api_key = "AIzaSyCxd-fwKs1lKk1tGp5SG61sdGg4p8SEZ7s"
# api_key = "AIzaSyDYRNQTPhPZm0R8nA_ivjJgFFwe9nCQfgY"
# api_key = "AIzaSyB2swKmvE7JYDdcUNgyYFJ1fLAFHu_Sfuk"
# api_key = "AIzaSyAm-m5MYn2-wcnLCytHe_aUWgXFnwH7M6E"
api_key = "AIzaSyB27pn1zUgB7lA2_vbkjDBoDZYuy7SP_l0"

logging.basicConfig(level=logging.INFO)


def insert_to_mongo_db(youtube):
    pass

    # insert_to_mongodb(dict_youtube)

    # client = connect_to_mongo_db()
    # logging.info("Available databases in mongo db: ")
    # logging.info(client.list_database_names())
    # db = client.YouTubeDB
    # youtube_collection = db.youtube

    # logging.info("Deleting the existing collections...")
    # youtube_collection.delete_many({})
    # logging.info("Deleted collections.")

    # logging.info("Inserting youtube data into collections...")
    # youtube_collection.insert_many(youtube)
    # logging.info("Inserted.")


def search_by_query(search_query, search_type):
    page_token = ""
    logging.info("Calling search API end point with query...")
    url = "https://www.googleapis.com/youtube/v3/search?key=" + api_key + "&q=" + search_query + "&type=" \
          + search_type + "&part=snippet"
    response = requests.get(url).json()

    next_page_token = response["nextPageToken"]
    video_ids = []

    # Each API call gets 5 results
    max_allowed_api_calls = 1
    counter = 0

    # create pandas dataframe
    cols = ["video_id", "title", "description", "transcript"]
    df_search = pd.DataFrame(columns=cols)

    while True:
        if counter == max_allowed_api_calls:
            break
        else:
            counter += 1
        logging.info("Making the " + str(counter) + ". API call...")
        url = "https://www.googleapis.com/youtube/v3/search?key=" + api_key + "&q=" + search_query + "&type=" \
              + search_type + "&part=snippet" + "&pageToken=" + page_token + "&maxResults=5"
        response = requests.get(url).json()

        if "nextPageToken" in response:
            page_token = response['nextPageToken']
        else:
            page_token = ""
            break

        if search_type == "video":
            for item in response['items']:
                # Option 1: save information in variables and add to dataframe
                video_id = item['id']['videoId']
                video_title = item['snippet']['title']
                video_description = item['snippet']['description']
                video_transcript = ""
                try:
                    # print(video_id)
                    # transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
                    # transcript_list = []
                    # for element in transcript:
                    # transcript_list.append(element['text'])
                    # video_transcript = '.'.join(transcript_list)

                    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
                    transcript_list = []
                    for element in transcript:
                        text = element['text']
                        text += "."
                        transcript_list.append(text)

                    # print(video_transcript)
                except Exception as e:
                    print(e)
                    transcript_list = []
                # Save data into pandas dataframe
                new_row = [video_id, video_title, video_description, transcript_list]
                df_new_row = pd.DataFrame([new_row], columns=cols)
                df_search = pd.concat([df_search, df_new_row], ignore_index=True)

                # Option 2: save same information type into list, then give as columns of the dataframe
                video_ids.append(item['id']['videoId'])

    logging.info("In total " + str(len(video_ids)) + " videos/results are collected.")
    # pd.set_option("display.max_rows", None, "display.max_columns", None)

    print(df_search)
    # print(tabulate(df, headers='keys', tablefmt='psql'))
    # print(tabulate(df, headers='keys', tablefmt='fancy_grid'))
    return df_search


API_COUNTER = 0

# def get_transcripts(df_new, search_query, phone_name, page_token, search_type, num):
#     max_results = num
#     global API_COUNTER
#     print("beginning")
#     print(API_COUNTER)
#
#     # keys = ["AIzaSyBSuf1z7mqV9-2IH5WbIJzkrsM5b2KHBMU", "AIzaSyD5_DJ3nv9CySefqkEZH3jVEzzzewuwKbw",
#     #         "AIzaSyDwBns_kxeusJEy1iU1L5aDbQ0GvbCA2tg", "AIzaSyAwBN7ZnVlzHTiG9e3s7XyFOdXefcDYKnk",
#     #         "AIzaSyCMhPvzt2_lAOAsypiBCVJ2_uEivENlTIo", "AIzaSyCxd-fwKs1lKk1tGp5SG61sdGg4p8SEZ7s",
#     #         "AIzaSyDYRNQTPhPZm0R8nA_ivjJgFFwe9nCQfgY", "AIzaSyB2swKmvE7JYDdcUNgyYFJ1fLAFHu_Sfuk",
#     #         "AIzaSyAm-m5MYn2-wcnLCytHe_aUWgXFnwH7M6E", "AIzaSyB27pn1zUgB7lA2_vbkjDBoDZYuy7SP_l0"]
#
#     cols = ["phone_name", "video_id", "transcript_list"]
#     # df_transcripts = pd.DataFrame(columns=cols)
#
#     # df_transcripts = df
#     url = "https://www.googleapis.com/youtube/v3/search?key=" + api_key + "&q=" + search_query + "&type=" \
#           + search_type + "&part=snippet" + "&maxResults=1" + "&pageToken=" + page_token
#     response = requests.get(url).json()
#
#     next_page_token = response["nextPageToken"]
#     # api_counter = 0
#     while API_COUNTER <= max_results:
#         print("df shape")
#         print(df_new.shape[0])
#         if df_new.shape[0] == max_results:
#             print("max reached")
#             print(df_new)
#             return df_new
#             # break
#             # write_transcripts_to_files(df_transcripts)
#         else:
#             if search_type == "video":
#                 for item in response['items']:
#                     # Option 1: save information in variables and add to dataframe
#                     video_id = item['id']['videoId']
#                     video_transcript = ""
#                     try:
#                         transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
#                         transcript_list = []
#                         for element in transcript:
#                             text = element['text']
#                             text += "."
#                             transcript_list.append(text)
#                     except Exception as e:
#                         print("Exception")
#
#                         transcript_list = []
#                     if not transcript_list:
#                         # list is empty
#                         get_transcripts(df_new, search_query, phone_name, next_page_token, search_type, max_results)
#                         print("list empty")
#                         print(API_COUNTER)
#                     else:
#                         print(video_id)
#                         print("list not empty")
#                         API_COUNTER += 1
#                         print(API_COUNTER)
#                         # print(transcript_list)
#                         cols = ["video_id", "phone_name", "transcript_list"]
#                         new_row = [video_id, phone_name, transcript_list]
#                         df_new_row = pd.DataFrame([new_row], columns=cols)
#                         df_new = pd.concat([df_new, df_new_row], ignore_index=True)
#                         print(df_new)
#                         print("in ")
#                         get_transcripts(df_new, search_query, phone_name, next_page_token, search_type, max_results)
#
#     # return df_transcripts

# global api_counter

# keys = ["AIzaSyBSuf1z7mqV9-2IH5WbIJzkrsM5b2KHBMU", "AIzaSyD5_DJ3nv9CySefqkEZH3jVEzzzewuwKbw",
#         "AIzaSyDwBns_kxeusJEy1iU1L5aDbQ0GvbCA2tg", "AIzaSyAwBN7ZnVlzHTiG9e3s7XyFOdXefcDYKnk",
#         "AIzaSyCMhPvzt2_lAOAsypiBCVJ2_uEivENlTIo", "AIzaSyCxd-fwKs1lKk1tGp5SG61sdGg4p8SEZ7s",
#         "AIzaSyDYRNQTPhPZm0R8nA_ivjJgFFwe9nCQfgY", "AIzaSyB2swKmvE7JYDdcUNgyYFJ1fLAFHu_Sfuk",
#         "AIzaSyAm-m5MYn2-wcnLCytHe_aUWgXFnwH7M6E", "AIzaSyB27pn1zUgB7lA2_vbkjDBoDZYuy7SP_l0"]

keys = ["AIzaSyD4NKDR7hSFzlfRYbG8sEuswCO3mk2oY44", "AIzaSyDOMhqaLhqYLpToburalRVvToTPHQBewOk"]


def get_transcripts(df_new, search_query, phone_name, page_token, search_type, num):
    global API_COUNTER

    max_results = num

    api_key = keys[0]
    cols = ["phone_name", "video_id", "transcript_list"]
    # df_transcripts = pd.DataFrame(columns=cols)

    # df_transcripts = df
    url = "https://www.googleapis.com/youtube/v3/search?key=" + api_key + "&q=" + search_query + "&type=" \
          + search_type + "&part=snippet" + "&maxResults=1" + "&pageToken=" + page_token
    response = requests.get(url).json()

    try:
        next_page_token = response["nextPageToken"]
    except KeyError:
        keys.pop(0)
        api_key = keys[0]
        url = "https://www.googleapis.com/youtube/v3/search?key=" + api_key + "&q=" + search_query + "&type=" \
              + search_type + "&part=snippet" + "&maxResults=1" + "&pageToken=" + page_token
        response = requests.get(url).json()
        next_page_token = response["nextPageToken"]

    # API_COUNTER = 0
    while API_COUNTER <= max_results:
        print("df shape")
        print(df_new.shape[0])
        if df_new.shape[0] == max_results:
            print("max reached")
            print(df_new)
            return df_new
            break
            # write_transcripts_to_files(df_transcripts)
        else:
            if search_type == "video":
                for item in response['items']:
                    # Option 1: save information in variables and add to dataframe
                    video_id = item['id']['videoId']
                    video_transcript = ""
                    try:
                        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
                        transcript_list = []
                        for element in transcript:
                            text = element['text']
                            text += "."
                            transcript_list.append(text)
                    except Exception as e:
                        print("Exception")

                        transcript_list = []
                    if not transcript_list:
                        # list is empty
                        get_transcripts(df_new, search_query, phone_name, next_page_token, search_type, max_results)
                        print("list empty")
                        print(API_COUNTER)
                    else:
                        print(video_id)
                        print("list not empty")
                        API_COUNTER += 1
                        print(API_COUNTER)
                        # print(transcript_list)
                        cols = ["video_id", "phone_name", "transcript_list"]
                        new_row = [video_id, phone_name, transcript_list]
                        df_new_row = pd.DataFrame([new_row], columns=cols)
                        # df_new = pd.concat([df_new, df_new_row], ignore_index=True)
                        print(df_new)
                        print("iin ")

                        client = MongoClient(
                            "mongodb+srv://odpp_user:Uu5VxTud3tkbklwT@atlascluster.aqrdbga.mongodb.net/?retryWrites=true&w=majority")
                        print("Available databases in mongo db: ")
                        print(client.list_database_names())
                        db = client.youtube_db
                        collection = db.transcripts
                        print(collection)

                        # mongo_data = pd.DataFrame(collection.find())
                        # if not mongo_data['video_id']:
                        #     if video_id not in mongo_data['video_id']:
                        dict_one_youtube = df_new_row.to_dict('records')

                        dictionary_name = {'video_id': video_id,
                                           'phone_name': phone_name,
                                           'transcript_list': transcript_list}

                        print("Inserting youtube entry into collection  ...")
                        collection.insert_one(dictionary_name)
                        print("Inserted.")
                        get_transcripts(df_new, search_query, phone_name, next_page_token, search_type, max_results)

    # return df_transcripts


def get_youtube_data_from_mongo():
    print("in get content from mongo")
    try:
        client = MongoClient(
            "mongodb+srv://odpp_user:Uu5VxTud3tkbklwT@atlascluster.aqrdbga.mongodb.net/?retryWrites=true&w=majority")

        print(client.list_database_names())
        db = client.youtube_db
        collection = db.transcripts
        data = pd.DataFrame(collection.find())
        print(data.head())
    except Exception as e:
        print(e)
    return data


def segment_test():
    # transcript = YouTubeTranscriptApi.get_transcript("g41ivRm1ABk&t=1s", languages=['en'])
    # print(transcript)

    transcript = YouTubeTranscriptApi.get_transcript("g41ivRm1ABk&t=1s", languages=['en'])
    transcript_list = []
    for element in transcript:
        text = element['text']
        text += "."
        transcript_list.append(text)
    # video_transcript = '.'.join(transcript_list)
    # print(video_transcript)
    print(transcript_list)


def test_write():
    data = [['tom', 10, 1], ['nick', 15, 2], ['juli', 14, 3]]

    # Create the pandas DataFrame
    df = pd.DataFrame(data, columns=['Name', 'Age', 'Semester'])

    # print dataframe.
    # print(df)
    sub = df[['Name', 'Semester']]
    # print(sub)

    for i in range(sub.shape[0]):
        # print(sub.loc[i])
        # print(sub.loc[i, 'Name'])
        file_name = sub.loc[i, 'Name']
        file_name += ".txt"
        print(file_name)
        file = open(file_name, "w")
        file.write(str(df.loc[i, 'Semester']))
        file.close()


def write_transcripts_to_files(df):
    print("change dir")
    transcripts_path = os.getcwd() + r'\transcripts'
    print(os.chdir(r'C:\Users\a892215\Projects\ODPP\ODPP\youtube_api\transcripts'))

    f = open("video_ids.txt", "w")
    for i in range(df.shape[0]):
        video_id = df.loc[i, 'video_id']
        f.write(video_id + '\n')

        file_name = video_id + ".txt"
        print(file_name)
        file = open(file_name, "w")
        text = ' '.join(df.loc[i, 'transcript'])
        # print(df.loc[i, 'transcript'])
        # print(type(df.loc[i, 'transcript']))
        file.write(text)
        file.close()
    f.close()


def update_transcripts():
    client = MongoClient(
        "mongodb+srv://odpp_user:Uu5VxTud3tkbklwT@atlascluster.aqrdbga.mongodb.net/?retryWrites=true&w=majority")
    print("Available databases in mongo db: ")
    print(client.list_database_names())
    db = client.youtube_db
    collection = db.transcripts
    print(collection)
    data = pd.DataFrame(collection.find())
    print(data.head())
    print(data.columns)

    tokenizer = AutoTokenizer.from_pretrained('oliverguhr/fullstop-punctuation-multilang-large')
    model = AutoModelForTokenClassification.from_pretrained('oliverguhr/fullstop-punctuation-multilang-large')

    pun = pipeline('ner', model=model, tokenizer=tokenizer)

    for index in data.index.values:
        print(data.loc[index, '_id'])
        document_id = data.loc[index, '_id']
        transcript = data.loc[index, 'transcript_list']
        transcript = ' '.join(transcript)
        output_json = pun(transcript)

        s = ''
        for n in output_json:
            result = n['word'].replace('▁', ' ') + n['entity'].replace('0', '')
            s += result
        print(s)
        result = collection.update_one({"_id": document_id}, {"$set": {"transcript_list": s}})


    # mongo_data = pd.DataFrame(collection.find())
    # if not mongo_data['video_id']:
    #     if video_id not in mongo_data['video_id']:
    # dict_one_youtube = df_new_row.to_dict('records')
    #
    # dictionary_name = {'video_id': video_id,
    #                    'phone_name': phone_name,
    #                    'transcript_list': transcript_list}
    #
    # print("Inserting youtube entry into collection  ...")
    # collection.insert_one(dictionary_name)
    # print("Inserted.")


if __name__ == '__main__':
    # df_ifixit = get_content_from_mongo()
    # phone_names = df_ifixit["brand"] + " " + df_ifixit["model"]
    # print(type(phone_names.values))
    # print(list(phone_names))
    # phone_names_list = list(phone_names)
    # cols = ["phone_name", "video_id", "transcript_list"]
    # print(phone_names)
    # query = "Teardown and Repair Assessment"
    # df_transcripts = pd.DataFrame(columns=cols)
    # df_col = pd.DataFrame(columns=cols)
    # phone_names_test = ["Google Pixel 6", "iPhone 12 Pro", "Samsung Galaxy Note"]
    #
    # first_ten = phone_names_list[0:5]
    # left_ones = phone_names_list[115:]
    # print(left_ones)
    # for name in left_ones:
    #     main_query = name + " " + query
    #     print(main_query)
    #     get_transcripts(df_transcripts, main_query, name, "", "video", 2)
    #     print("in the for loop:" + name)

    update_transcripts()
