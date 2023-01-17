import streamlit as st
import os, sys
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import requests

# appending the parent directory path
# sys.path.append(r'C:\Users\a892215\Projects\ODPP\ODPP\visualization')
#
# # importing the methods
# from visualization.web_scraper_ifixit import get_content_from_mongo


st.set_page_config(page_title="Channel Statistics", page_icon="📈")

st.markdown("# Channel Statistics 📈")
st.sidebar.header("")
st.write(
    """We are using Google API Python client library to interact with the YouTube API and retrieve channel statistics.\n
The channel_statistics variable will contain a dictionary with various statistics about the channel, such as the number of subscribers, views, and comments.  \n
We are retrieving the channel statistics of four most known YouTube channels of phone repairments.
    """
)

# API_KEY = "AIzaSyCMhPvzt2_lAOAsypiBCVJ2_uEivENlTIo"
API_KEY = "AIzaSyCxd-fwKs1lKk1tGp5SG61sdGg4p8SEZ7s"
# API_KEY = "AIzaSyDYRNQTPhPZm0R8nA_ivjJgFFwe9nCQfgY"
IFIXIT = 'UCHbx9IUW7eCeJsC4sBCTNBA'
PHONE_REPAIR_GURU = 'UCCOrp7GPgZA8EGrbOcIAsyQ'
MOBILE_REPAIRING_TUTORIAL = 'UCWbFVuq9hgJDX2fxIlkLLFQ'
HUGH_JEFFREY = 'UCQDhxkSxZA6lxdeXE19aoRA'

channels = [IFIXIT, PHONE_REPAIR_GURU, MOBILE_REPAIRING_TUTORIAL, HUGH_JEFFREY]
channel_dictionary = {'iFixIt': 'UCHbx9IUW7eCeJsC4sBCTNBA',
                      'Phone Repair Guru': 'UCCOrp7GPgZA8EGrbOcIAsyQ',
                      'Mobile Repairing Tutorial': 'UCWbFVuq9hgJDX2fxIlkLLFQ',
                      'Hugh Jeffrey': 'UCQDhxkSxZA6lxdeXE19aoRA', }


def load_channels():
    client = MongoClient(
        "mongodb+srv://odpp_user:Uu5VxTud3tkbklwT@atlascluster.aqrdbga.mongodb.net/?retryWrites=true&w=majority")
    print("Available databases in mongo db: ")
    print(client.list_database_names())
    db = client.youtube_db
    collection = db.channels

    data = pd.DataFrame(collection.find())
    print(data.head())
    return data


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

st.dataframe(df)

# for key, value in channel_dictionary.items():
#     counter = 0

list = ['repair', 'teardown', 'Teardown', 'Tear down', 'Tear-down']
data = load_channels()
# filtered_df = data[if data['Title'] in list]
grouped_df = df.groupby('Channel Name')


labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
sizes = [15, 30, 45, 10]
explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

st.pyplot(fig1)

# data = load_channels()
