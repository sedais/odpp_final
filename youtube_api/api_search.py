import requests
import logging
import pandas as pd
import torch
import sys
import os
from youtube_transcript_api import YouTubeTranscriptApi

# Keys
# api_key = "AIzaSyBSuf1z7mqV9-2IH5WbIJzkrsM5b2KHBMU"
# api_key = "AIzaSyD5_DJ3nv9CySefqkEZH3jVEzzzewuwKbw"
# api_key = "AIzaSyDwBns_kxeusJEy1iU1L5aDbQ0GvbCA2tg"
api_key = "AIzaSyAwBN7ZnVlzHTiG9e3s7XyFOdXefcDYKnk"
# api_key = "AIzaSyCMhPvzt2_lAOAsypiBCVJ2_uEivENlTIo"
logging.basicConfig(level=logging.INFO)


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


def get_transcripts(df, search_query, page_token, search_type, num):
    global API_COUNTER

    max_results = num
    df_transcripts = df
    url = "https://www.googleapis.com/youtube/v3/search?key=" + api_key + "&q=" + search_query + "&type=" \
          + search_type + "&part=snippet" + "&maxResults=1" + "&pageToken=" + page_token
    response = requests.get(url).json()

    next_page_token = response["nextPageToken"]

    while api_counter <= max_results:
        print("df shape")
        print(df_transcripts.shape[0])
        if df_transcripts.shape[0] == max_results:
            print("max reached")
            print(df_transcripts)
            write_transcripts_to_files(df_transcripts)
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
                    get_transcripts(df_transcripts, search_query, next_page_token, search_type, max_results)
                    print("list empty")
                    print(api_counter)
                else:
                    print(video_id)
                    print("list not empty")
                    api_counter += 1
                    print(api_counter)
                    # print(transcript_list)
                    new_row = [video_id, transcript_list]
                    df_new_row = pd.DataFrame([new_row], columns=cols)
                    df_transcripts = pd.concat([df_transcripts, df_new_row], ignore_index=True)
                    print(df_transcripts)
                    get_transcripts(df_transcripts, search_query, next_page_token, search_type, max_results)

    #return df_transcripts

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


if __name__ == '__main__':
    query = "change phone battery"
    types = ["channel", "playList", "video"]
    # for t in types:
    #    search_by_query(query, t)

    arg_query = ""
    for i in range(1, len(sys.argv)):
        val = str(sys.argv[i])
        arg_query += val + " "

    print(arg_query)
    # df = search_by_query(arg_query, "video")
    # write_transcripts_to_files(df)

    global API_COUNTER
    API_COUNTER = 0

    cols = ["video_id", "transcript"]
    df_transcripts = pd.DataFrame(columns=cols)
    a_query = query + " " + arg_query
    print(a_query)
    df = get_transcripts(df_transcripts, a_query, "", "video", 5)

    print("main")
    print(os.getcwd())


    # print(df)
    # print(tabulate(df, headers='keys', tablefmt='fancy_grid'))

    # test_write()
