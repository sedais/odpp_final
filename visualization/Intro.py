import streamlit as st
from keybert import KeyBERT
from youtube_api import get_transcripts
from web_scraper_ifixit import get_the_content
from streamlit_sortables import sort_items

import seaborn as sns
import pandas as pd
import numpy as np
import altair as alt

import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
import pandas as pd
from bs4 import BeautifulSoup
import requests

import pymongo
import ssl
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import certifi

nlp = spacy.load('en_core_web_sm')
nlp.add_pipe('spacytextblob')

st.set_page_config(
    page_title="ODPP",
    page_icon="🚀",
)

st.write("# Welcome to (Open) Digital Product Pass Social Media Analysis Results! 🚀")


with st.expander("ℹ️ - About this app", expanded=True):
    st.write(
        """     
   -   This  app is an easy-to-use interface built in Streamlit utilized to show EDA and Sentiment Analysis Results developed for analyzing YouTube transcript data.
           """
    )

    st.markdown("")


st.subheader("IFixIt")

st.write("""
- iFixit is a global community of people helping each other repair devices with a mission to make repair accessible and easy for as many people around the world as possible. Including the approach of “the easier it is to fix something; the more people will do it.“.
- Aims to decrease electronic waste and the toxic legacy of our digital age
- IFixIt shows also an important engagement in the YouTube community with over 989K subscribers
""")

st.subheader("Repairability Scores")
st.write("""
Based on if:
- internal components are easy to open for access 
- battery can be replaced without any tools
- removing internal components requires specialty screwdrivers and knowledge of the adhesive removal technique
""")



@st.cache
def load_ifixit_data():
    data = get_the_content()
    return data


@st.cache
def load_youtube_data():
    # cols = ["phone_name", "video_id", "transcript"]
    # query = "change phone battery"
    # phone_db = get_the_content()
    # phone_names = phone_db["brand"] + " " + phone_db["model"]
    # print("in load youtube data")
    # print(phone_names)
    #
    # df_transcripts = pd.DataFrame(columns=cols)
    # phone_names_test = ["Google Pixel 6", "iPhone 12 Pro", "Samsung Galaxy Note"]
    # for name in phone_names_test:
    #     a_query = query + " " + name
    #     print(a_query)
    #     df = get_transcripts(df_transcripts, a_query, "", "video", 1)
    #     #df['phone_name'] = name
    #     df.loc[:, 'phone_name'] = name
    #     #df_transcripts = df_transcripts + df
    # data = df
    print("I'm in load youtube data")
    # client = MongoClient(
    #     "mongodb+srv://sedaismail:1234@cluster0.65tresj.mongodb.net/?retryWrites=true&w=majority",
    #     server_api=ServerApi('1'))

    print("Available databases in mongo db: ")

    client = MongoClient(
        "mongodb+srv://sedaismail:12345@cluster0.65tresj.mongodb.net/?retryWrites=true&w=majority")
    db = client.test

    # client = pymongo.MongoClient(
    #     "mongodb+srv://Python:hQTMon51YyXJjzLT@odpp.proeq78.mongodb.net/?retryWrites=true&w=majority")
    # db = client.PhoneDB

    print(client.list_database_names())
    db = client.YouTubeDB
    collection = db.youtube
    data = pd.DataFrame(collection.find())
    print("i am in load youtube data")
    print(data)
    return data


def main():
    st.header("This is the main page")
    st.write("Here you can find some information about our company.")


def ifixit():
    st.header("IFixIt Keyword extraction from the facts and the sentiment scores regarding the facts")
    st.write("Here you can find the complete data from IFixIt")
    data = load_ifixit_data()
    print(data.head())

    # Display an interactive table
    st.dataframe(data)

    st.write("Here you can find the keyword extraction for each phone")

    kw_model = KeyBERT()
    facts_list = []
    data = get_the_content()
    print(data.head())
    data["facts_doc"] = data["fact1"] + " " + data["fact1"] + " " + data["fact1"]
    print(data.head())

    keywords_list = []
    print(data.head())
    for index in data.index.values:
        # print(data.iloc[index]["facts_doc"])
        facts_list = data.iloc[index]["facts_doc"]
        keywords = kw_model.extract_keywords(facts_list, keyphrase_ngram_range=(1, 3), stop_words="english")
        keywords_list.append(keywords)
        # print(keywords)

    data["keywords"] = keywords_list
    print(data.head())

    kw_name_list = []
    kw_relevancy_list = []

    for ind in data.index:
        kw = data['keywords'][ind]
        for elem in kw:
            kw_name = elem[0]
            kw_name_list.append(kw_name)
            kw_relevancy = elem[1]
            kw_relevancy_list.append(kw_relevancy)
        df = pd.DataFrame(list(zip(kw_name_list, kw_relevancy_list)),
                          columns=["Keyword/Key phrase", "Relevancy"]).sort_values(by="Relevancy",
                                                                                   ascending=False).reset_index(
            drop=True)

        # get only 2 keywords with the highest score
        df = df.iloc[0:2, :]
        print(df)
        kw_name_list.clear()
        kw_relevancy_list.clear()

        # Add styling
        cmGreen = sns.light_palette("green", as_cmap=True)
        cmRed = sns.light_palette("red", as_cmap=True)
        df = df.style.background_gradient(
            cmap=cmGreen,
            subset=[
                "Relevancy",
            ],
        )

        # c1, c2, c3 = st.columns([1, 3, 1])

        format_dictionary = {
            "Relevancy": "{:.1%}",
        }

        df = df.format(format_dictionary)
        print("here")
        print(df)
        st.subheader(data['brand'][ind] + " " + data['model'][ind])
        st.table(df)


def ifixit_sentiment():
    print("in fix sentiment")
    data = load_ifixit_data()
    print(data.head())
    s = data['score'].value_counts().sort_index()
    df_chart = s.to_frame()
    st.subheader("Count of Phones by Scores")
    st.bar_chart(df_chart)

    s2 = data.groupby(['brand'])['score'].mean()
    data_mean = s2.to_frame().reset_index()
    data_mean['score'] = round(data_mean['score'], 2)
    data_mean = data_mean.sort_values(by=['score'], ascending=False)
    print(data_mean.head())
    st.subheader("Average Score by Brand")
    st.bar_chart(data_mean, x='brand', y='score')


def youtube():
    st.header("YouTube Text Extraction")
    st.write("Here you can find keywords from the youtube video transcripts")

    print("here in youtube text extraction")
    data = load_youtube_data()
    print(data.head())

    for index in data.index.values:
        transcript = data.iloc[index]["transcript_list"]
        texts = " ".join(str(x) for x in transcript)

        kw_model = KeyBERT()

        keywords_list = []

        keywords = kw_model.extract_keywords(texts, keyphrase_ngram_range=(1, 3), stop_words="english")
        keywords_list.append(keywords)
        print(keywords)
        print(keywords_list)

        # data["keywords"] = keywords_list
        # print(data.head())

        kw_name_list = []
        kw_relevancy_list = []

        for elem in keywords_list:
            kw_name = elem[0]
            kw_name_list.append(kw_name)
            kw_relevancy = elem[1]
            kw_relevancy_list.append(kw_relevancy)

        df = pd.DataFrame(list(zip(kw_name_list, kw_relevancy_list)),
                          columns=["Keyword/Keyphrase", "Relevancy"]).sort_values(by="Relevancy",
                                                                                  ascending=False).reset_index(
            drop=True)

        # get only 2 keywords with the highest score
        df = df.iloc[0:2, :]
        print(df)
        kw_name_list.clear()
        kw_relevancy_list.clear()

        # Add styling
        cmGreen = sns.light_palette("green", as_cmap=True)
        cmRed = sns.light_palette("red", as_cmap=True)
        df = df.style.background_gradient(
            cmap=cmGreen,
            subset=[
                "Relevancy",
            ],
        )

        # c1, c2, c3 = st.columns([1, 3, 1])

        format_dictionary = {
            "Relevancy": "{:.1%}",
        }

        df = df.format(format_dictionary)
        print("here")
        print(df)
        st.subheader("sth")
        st.table(df)


def youtube_sentiment():
    st.header("Here you can find YouTube Sentiment Analysis Results!")
    st.write(
        "We use python's spaCy library for NLP, is designed specifically for production use and helps you build "
        "applications that process and “understand” large volumes of text, to get the sentiment label and scores")

    option = st.selectbox(
        'How would you like to be contacted?',
        ('Email', 'Home phone', 'Mobile phone'))

    st.write('You selected:', option)

    data = load_youtube_data()

    phone_names = []
    sent_score = []
    sent_label = []
    total_pos = []
    total_neg = []

    for index in data.index.values:
        transcript = data.iloc[index]["transcript_list"]
        phone_name = data.iloc[index]["phone_name"]
        phone_names.append(phone_name)

        print(phone_name)
        print("i am in sentiment")
        # print(transcript)
        texts = " ".join(str(x) for x in transcript)
        # print(texts)
        doc = nlp(texts)
        sentiment = doc._.blob.polarity
        sentiment = round(sentiment, 2)
        print("sentiment is")

        print(sentiment)
        if sentiment > 0:
            label = "Positive"
        else:
            label = "Negative"

        sent_label.append(label)
        sent_score.append(sentiment)

        positive_words = []
        negative_words = []
        df_row = pd.DataFrame()
        df_final = pd.DataFrame()

        for x in doc._.blob.sentiment_assessments.assessments:
            if x[1] > 0:
                positive_words.append(x[0][0])
            elif x[1] < 0:
                negative_words.append(x[0][0])
            else:
                pass

        total_pos.append(', '.join(set(positive_words)))
        total_neg.append(', '.join(set(negative_words)))

        df_row = df_row.iloc[0:0]
        # print(df_row)
        print(phone_name)
        print(sent_score)
        print(sent_label)

        df_row["Phone Name"] = phone_names
        df_row["Sentiment Score"] = sent_score
        df_row["Sentiment Label"] = sent_label
        df_row["Positive Words"] = total_pos
        df_row["Negative Words"] = total_neg
        print(df_row)
        df_final = pd.concat([df_final, df_row], ignore_index=True)

    st.subheader("Sentiment Results")
    # st.table(df_final)
    st.dataframe(df_final)


# Add a sidebar to the app with links to the two pages
# st.sidebar.title("Navigation")
# page = st.sidebar.radio("Go to",
#                         ["Main", "IFixIt Text Extraction", "IFixIt Sentiment Analysis", "Youtube Text Extraction",
#                          "YouTube Sentiment Analysis"])
#
# if page == "IFixIt Text Extraction":
#     ifixit()
# elif page == "IFixIt Sentiment Analysis":
#     ifixit_sentiment()
# elif page == "Youtube Text Extraction":
#     youtube()
# elif page == "YouTube Sentiment Analysis":
#     youtube_sentiment()

# load_ifixit_data()
# load_youtube_data()

st.subheader("IFixIt Repairability Scores Data")
st.write("Their data and summarized results give key information about the phones that are regularly used this day")
st.write("To see the document please go to [this page](https://www.ifixit.com/smartphone-repairability?sort=date) or scroll down for the same results displayed here.")
data = load_ifixit_data()
st.dataframe(data)