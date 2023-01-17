import streamlit as st
from pymongo import MongoClient
from nltk.tokenize import word_tokenize, sent_tokenize
import pandas as pd
import tabulate


def load_sentiment_data():
    print("Getting video data from youtube_db in mongo...")
    try:
        # Connect to the MongoDB server
        client = MongoClient(
            "mongodb+srv://odpp_user:lo0fVGfZLPZtWvQB@cluster0.65tresj.mongodb.net/?retryWrites=true&w=majority")
        db = client.youtube_db
        collection = db.videos
        data = pd.DataFrame(collection.find())

        texts_reduced = []
        list = ['repair', 'healthy', 'battery', 'change', 'remove', 'removed', 'removal', 'easy', 'hard', 'repair',
                'repairability']

        for index in data.index.values:
            doc = data.loc[index, 'transcript_punctuated']
            # doc = ' '.join(doc)
            sentences_with_word = []
            for sen in sent_tokenize(doc):
                l = word_tokenize(sen)

                if len(set(l).intersection(list)) > 0:
                    sentences_with_word.append(sen)
            # print(sentences_with_word)
            texts_reduced.append(sentences_with_word)
        data["text_reduced"] = texts_reduced
    except Exception as e:
        print(e)

    print("Youtube data loaded successfully")
    print(data)
    # print(data.loc[0, 'text_reduced'])
    print(data.columns)

    return data


def get_youtube_sentiment_data():
    # data = load_data_youtube()
    # data = load_youtube_sentiment_data()
    data = load_sentiment_data()

    phone_names = data['brand'] + " " + data['model']
    no_dub = phone_names.unique().tolist()

    # phone_selection = st.sidebar.selectbox('Select a phone', [''] + sorted(no_dub))
    # print("Phone selected" + phone_selection)
    # brand = phone_selection.split(" ")[0]
    # model = phone_selection.split(" ")[1:]
    brand = "Apple"
    model = "iPhone 14 Plus"

    sentiment_types = ['All', 'spaCy', 'GCP', 'Roberta', 'Siebert']
    sentiment_selection = st.sidebar.selectbox('Select a sentiment analysis method', [''] + sentiment_types)
    print("Sentiment selected")

    # data_sentiment = data['text_reduced']
    # sentiment1_list = []

    # print(selection)
    print(data.columns)
    print(data['gcp magnitude'])

    # print("in gcp")
    # df_sentiment = data[
    #     ['video_id', 'brand', 'model', 'title', 'description', 'channel_title', 'gcp score', 'gcp magnitude']]
    # print("df_sentiment")
    # print(df_sentiment)
    # print(
    #     "Sentiment Analysis of first three videos of YouTube Teardown and Repair Assessment search for")
    # # print(df_sentiment[df_sentiment['brand'] == brand])
    # print(df_sentiment[(df_sentiment['model'] == model) & (df_sentiment['brand'] == brand)])
    # (df_sentiment[df_sentiment['brand'] == brand]))

    print("in spaCy")
    df_sentiment = data[
        ['video_id', 'brand', 'model', 'title', 'description', 'channel_title', 'spacy polarity', 'spacy subjectivity']]
    print(df_sentiment)
    print(df_sentiment[(df_sentiment['model'] == model) & (df_sentiment['brand'] == brand)].drop_duplicates())

    print(data.columns)
    df_statistics = data[['video_id', 'brand', 'model', 'title', 'description', 'channel_title', 'view count']]
    #                     'like count', 'comment count']
    print(df_statistics)

    df_texts = data[['video_id', 'brand', 'model', 'title', 'description', 'texts_filtered']].drop_duplicates()
    print(df_texts)
    #print(df_texts[(df_texts['model'] == model) & (df_texts['brand'] == brand)].drop_duplicates())


if __name__ == '__main__':
    get_youtube_sentiment_data()
    # data = load_sentiment_data()
    # print(data[310:]['gcp score'])