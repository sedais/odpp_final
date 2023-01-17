from google.oauth2.credentials import Credentials
import requests
import pandas as pd
from tabulate import tabulate
from pymongo import MongoClient

# API_KEY = "AIzaSyB27pn1zUgB7lA2_vbkjDBoDZYuy7SP_l0"
# API_KEY = "AIzaSyBSuf1z7mqV9-2IH5WbIJzkrsM5b2KHBMU"
# API_KEY = "AIzaSyD5_DJ3nv9CySefqkEZH3jVEzzzewuwKbw"
API_KEY = "AIzaSyDwBns_kxeusJEy1iU1L5aDbQ0GvbCA2tg"
# API_KEY = "AIzaSyAwBN7ZnVlzHTiG9e3s7XyFOdXefcDYKnk"
# API_KEY = "AIzaSyCMhPvzt2_lAOAsypiBCVJ2_uEivENlTIo"
# API_KEY = "AIzaSyCxd-fwKs1lKk1tGp5SG61sdGg4p8SEZ7s"
# API_KEY = "AIzaSyDYRNQTPhPZm0R8nA_ivjJgFFwe9nCQfgY"
# API_KEY = "AIzaSyB2swKmvE7JYDdcUNgyYFJ1fLAFHu_Sfuk"
# API_KEY = "AIzaSyAm-m5MYn2-wcnLCytHe_aUWgXFnwH7M6E"

IFIXIT = 'UCHbx9IUW7eCeJsC4sBCTNBA'
PHONE_REPAIR_GURU = 'UCCOrp7GPgZA8EGrbOcIAsyQ'
MOBILE_REPAIRING_TUTORIAL = 'UCWbFVuq9hgJDX2fxIlkLLFQ'
HUGH_JEFFREY = 'UCQDhxkSxZA6lxdeXE19aoRA'


def get_channel_statistics(channelId):
    url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channelId}&key={API_KEY}'
    response = requests.get(url)
    #print(response.json()['items'])
    channel_statistics = response.json()['items'][0]['statistics']
    print(channel_statistics)


def get_video_details(channelId):
    url = f'https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={channelId}&part=snippet,id&order=date&maxResults=50&type=video'

    videos, video_ids, titles, descriptions, publish_dates = [], [], [], [], []

    while url:
        response = requests.get(url)
        data = response.json()
        videos.extend(data['items'])
        if 'nextPageToken' in data:
            url = f'{url}&pageToken={data["nextPageToken"]}'
        else:
            url = None

    # Print the titles of the videos
    for video in videos:
        video_ids.append(video['id']['videoId'])
        titles.append(video['snippet']['title'])
        descriptions.append(video['snippet']['description'])
        publish_dates.append(video['snippet']['publishedAt'])

        # print(video['snippet']['title'])
    return video_ids, titles, descriptions, publish_dates


def insert_channel_statistics_to_mongo(df):
    try:
        client = MongoClient(
            "mongodb+srv://odpp_user:Uu5VxTud3tkbklwT@atlascluster.aqrdbga.mongodb.net/?retryWrites=true&w=majority")
        print("Available databases in mongo db: ")
        print(client.list_database_names())
        db = client.youtube_db
        collection = db.channels
        print(collection)
        print("Deleting the existing collections...")
        collection.delete_many({})
        print("Deleted collections.")

        dict = df.to_dict('records')

        print("Inserting sentiments data into collection...")
        collection.insert_many(dict)
        print("Inserted.")

    except Exception as e:
        print(e)
    else:
        print("Connection is successful")


if __name__ == '__main__':
    channels = [IFIXIT, PHONE_REPAIR_GURU, MOBILE_REPAIRING_TUTORIAL, HUGH_JEFFREY]

    # Create a dictionary with two key-value pairs
    channel_dictionary = {'iFixIt': 'UCHbx9IUW7eCeJsC4sBCTNBA',
                          'Phone Repair Guru': 'UCCOrp7GPgZA8EGrbOcIAsyQ',
                          'Mobile Repairing Tutorial': 'UCWbFVuq9hgJDX2fxIlkLLFQ',
                          'Hugh Jeffrey': 'UCQDhxkSxZA6lxdeXE19aoRA', }

    # Create an empty DataFrame
    # df = pd.DataFrame()
    #
    # for key, value in channel_dictionary.items():
    #     video_ids, titles, descriptions, publish_dates = get_video_details(value)
    #     # Add a new row to the DataFrame
    #
    #     for i in range(len(titles)):
    #         df = df.append({'Channel Name': key, 'Video Id': video_ids[i], 'Title': titles[i], 'Description': descriptions[i],
    #                         'Publish Date': publish_dates[i]}, ignore_index=True)
    #         # new_row = pd.DataFrame({'Channel Name': key, 'Title': titles[i], 'Description': descriptions[i], 'Publish Date': publish_dates[i]}, ignore_index=True)
    #         # df = pd.concat([df, new_row], ignore_index=True)
    #
    # print(df)
    # print(df.shape)
    # print(tabulate(df, headers='keys', tablefmt='psql'))

    # insert_channel_statistics_to_mongo(df)
    for channel in channels:
        get_channel_statistics(channel)

    df = pd.DataFrame()
    for key, value in channel_dictionary.items():
        url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={value}&key={API_KEY}'
        response = requests.get(url)
        channel_statistics = response.json()['items'][0]['statistics']
        new_row = pd.DataFrame([
            {'Channel Name': key,
             'View Count': channel_statistics['viewCount'],
             'Subscriber Count': channel_statistics['subscriberCount'],
             'Video Count': channel_statistics['videoCount']}])
        df = pd.concat([df, new_row], ignore_index=True)
        # df = df.append({'Channel Name': key,
        #      'View Count': channel_statistics['viewCount'],
        #      'Subscriber Count': channel_statis<tics['subscriberCount'],
        #      'Video Count': channel_statistics['videoCount']}, ignore_index=True)

    print(df)
    # for channel in channels:
    #     titles, descriptions, publish_date = get_video_details(IFIXIT)
    #     df['Channel Name'] =
    #
    #     # Add a new row to the DataFrame
    #     df = df.append({'Channel Name': channel.lower(), 'B': 2, 'C': 3}, ignore_index=True)
    #     df[value] = value
