import streamlit as st
import pandas as pd

from nltk.tokenize import word_tokenize, sent_tokenize
from pymongo import MongoClient

st.set_page_config(page_title="Text Extraction", page_icon=" 🔑")

st.markdown("# Text Extraction 🔑")
st.sidebar.header("Text Extraction")
st.write(
    """This pages illustrates the result of text extraction analysis done with the [KeyBERT](https://towardsdatascience.com/enhancing-keybert-keyword-extraction-results-with-keyphrasevectorizers-3796fa93f4db)
     KeyBERT is an easy-to-use Python package for keyphrase extraction with BERT language models."""
)


def get_youtube_data_mongo():
    print("getting youtube data from mongo...")
    try:
        client = MongoClient(
            "mongodb+srv://odpp_user:Uu5VxTud3tkbklwT@atlascluster.aqrdbga.mongodb.net/?retryWrites=true&w=majority")

        print(client.list_database_names())
        db = client.youtube_db
        collection = db.transcripts
        data = pd.DataFrame(collection.find())
        print("mongodb data")
        print(data)
        transcript_texts = []
        for index in data.index.values:
            # print(data.iloc[index]["facts_doc"])
            transcript_text = data.iloc[index]["transcript_list"]
            transcript_text = '.'.join(transcript_text)
            transcript_texts.append(transcript_text)
        data["text"] = transcript_texts

        texts_reduced = []
        list = ['repair', 'healthy', 'battery', 'change', 'remove', 'removal', 'easy', 'hard', 'repair',
                'repairability']

        for index in data.index.values:
            doc = data.loc[index, 'transcript_list']
            doc = ' '.join(doc)
            sentences_with_word = []
            for sen in sent_tokenize(doc):
                l = word_tokenize(sen)

                if len(set(l).intersection(list)) > 0:
                    sentences_with_word.append(sen)
            texts_reduced.append(sentences_with_word)
        data["text_important"] = texts_reduced
        data_subset = data[['video_id', 'phone_name', 'text_important']]
        return data_subset
    except Exception as e:
        print(e)
    print("youtube data loaded successfully")


data = get_youtube_data_mongo()
st.dataframe(data)
