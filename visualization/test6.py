from nltk.tokenize import word_tokenize, sent_tokenize
from keybert import KeyBERT
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax
from pymongo import MongoClient
import pandas as pd
from transformers import pipeline

import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
import pandas as pd

nlp = spacy.load('en_core_web_sm')
nlp.add_pipe('spacytextblob')

client = MongoClient(
    "mongodb+srv://odpp_user:Uu5VxTud3tkbklwT@atlascluster.aqrdbga.mongodb.net/?retryWrites=true&w=majority")

print(client.list_database_names())
db = client.youtube_db
collection = db.transcripts
data = pd.DataFrame(collection.find())
transcript_texts = []
for index in data.index.values:
    # print(data.iloc[index]["facts_doc"])
    transcript_text = data.iloc[index]["transcript_list"]
    transcript_text = '.'.join(transcript_text)
    transcript_texts.append(transcript_text)
data["text"] = transcript_texts

texts_reduced = []
list = ['repair', 'battery']

for index in data.index.values:
    doc_new = data.loc[index, 'transcript_list']
    doc_new = ' '.join(doc_new)
    sentences_with_word = []
    for sen in sent_tokenize(doc_new):
        l = word_tokenize(sen)

        if len(set(l).intersection(list)) > 0:
            sentences_with_word.append(sen)
    # print(sentences_with_word)
    texts_reduced.append(sentences_with_word)
data["text_reduced"] = texts_reduced
data_subset = data[['video_id', 'phone_name', 'text_reduced']]

print(data_subset.head())

# sent = ' '.join(sentences_with_word)
# print(sent)

tranformers_pip_list = []

# for index in data_subset.index.values:
#     doc = data_subset.loc[index, 'text_reduced']
#     doc = ' '.join(doc)
#     sent_pipeline = pipeline("sentiment-analysis")
#     sentiment = sent_pipeline(doc)
#     tranformers_pip_list.append(sentiment)

# doc = data_subset.loc[3, 'text_reduced']
# doc = ' '.join(doc)
# sent_pipeline = pipeline("sentiment-analysis")
# sentiment = sent_pipeline(doc)
# print(sentiment)

#data_subset["transformers"] = tranformers_pip_list
# print(data_subset)
# sent_pipeline = pipeline("sentiment-analysis")
# print(sent_pipeline("i love me"))
print("---------------------------------------")
phone_names = []
sent_score = []
sent_label = []
total_pos = []
total_neg = []

for index in data_subset.index.values:

    transcript = data_subset.loc[index]["text_reduced"]
    phone_name = data.loc[index]["phone_name"]
    phone_names.append(phone_name)

    print(phone_name)
    print("i am in sentiment")
    # print(transcript)
    texts = " ".join(transcript)
    # print(texts)

    doc = nlp(texts)
    sentiment = doc._.blob.polarity
    sentiment = round(sentiment, 2)
    print("sentiment is")

    # doc = data_subset.loc[index, 'text_reduced']
    # #     doc = ' '.join(doc)
    # doc_new = nlp(doc)
    # sentiment = doc_new._.blob.polarity
    # sentiment = round(sentiment, 2)
    # print("sentiment is")

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

print(df_final.head())