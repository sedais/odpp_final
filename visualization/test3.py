import pandas as pd
import requests

IFIXIT = 'UCHbx9IUW7eCeJsC4sBCTNBA'
PHONE_REPAIR_GURU = 'UCCOrp7GPgZA8EGrbOcIAsyQ'
MOVILONE_MOBILE_REPAIR = 'UC3fkKCLVhc78HMgrI0gy9xA'
MOBILE_REPAIRING_TUTORIAL = 'UCWbFVuq9hgJDX2fxIlkLLFQ'
HUGH_JEFFREY = 'UCQDhxkSxZA6lxdeXE19aoRA'
API_KEY = "AIzaSyB2swKmvE7JYDdcUNgyYFJ1fLAFHu_Sfuk"

# Create a list of values
values = [1, 2, 3, 4, 5]

# Create an empty DataFrame
df = pd.DataFrame()

# Iterate over the list and assign the values to a column
# for value in values:
#     df[value] = value
df["value"] = values

print(df)

channels = [IFIXIT, PHONE_REPAIR_GURU, MOVILONE_MOBILE_REPAIR, MOBILE_REPAIRING_TUTORIAL, HUGH_JEFFREY]
for channel in channels:
    channel = channel.lower().replace("_", " ")

print(channels)
channelId= 'UCHbx9IUW7eCeJsC4sBCTNBA'
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
    #video_ids.append(video['id']['videoId'])
    print(video['id']['videoId'])
