import os
from functools import reduce

import pandas as pd
import spacy
from google.cloud import language_v1
from nltk.tokenize import word_tokenize, sent_tokenize
from pymongo import MongoClient
from scipy.special import softmax
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer
from transformers import pipeline


def insert_all_sentiments_mongo(gcp, spcy, roberta, siebert):
    try:
        client = MongoClient(
            "mongodb+srv://odpp_user:Uu5VxTud3tkbklwT@atlascluster.aqrdbga.mongodb.net/?retryWrites=true&w=majority")
        print("Available databases in mongo db: ")
        print(client.list_database_names())
        db = client.youtube_db
        collection = db.sentiment
        print(collection)

        # phone_names = df_ifixit["brand"] + " " + df_ifixit["model"]
        # print(type(phone_names.values))
        # print(list(phone_names))

        print("Deleting the existing collections...")
        collection.delete_many({})
        print("Deleted collections.")

        # define list of DataFrames
        df_sentiments = [gcp, spcy, roberta, siebert]

        #df_sentiments = [gcp, spcy, siebert]

        # merge all DataFrames into one
        final_df = reduce(lambda left, right: pd.merge(left, right, on=['Video Id', 'Phone Name'],
                                                       how='inner'), df_sentiments)

        print("Final DF!!")
        print(final_df)
        dict_final = final_df.to_dict('records')

        print("Inserting sentiments data into collection...")
        collection.insert_many(dict_final)
        print("Inserted.")

    except Exception as e:
        print(e)
    else:
        print("Test connection is successful")


def insert_gcp_to_mongo(df_gcp):
    client = MongoClient(
        "mongodb+srv://odpp_user:Uu5VxTud3tkbklwT@atlascluster.aqrdbga.mongodb.net/?retryWrites=true&w=majority")

    print(client.list_database_names())
    db = client.youtube_db
    collection = db.transcripts
    data = pd.DataFrame(collection.find())
    gcp_list = df_gcp['Sentiment Score']
    for index in data.index.values:
        # collection.update_one({"$set" : {"gcp_score" :gcp_list[index]}})
        print(gcp_list[index])
    print("is it updated?")


def get_gcp_results(data):
    print("getting gcp results")
    os.environ[
        "GOOGLE_APPLICATION_CREDENTIALS"] = r'C:\Users\a892215\Projects\ODPP\ODPP\visualization\pages\gcp-nlp-373009-64952e234ff1.json'
    client = language_v1.LanguageServiceClient()
    text = "i love my life"
    document = language_v1.Document(content=text, type=language_v1.Document.Type.PLAIN_TEXT)
    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(
        request={"document": document}
    ).document_sentiment

    print("Text: {}".format(text))
    print("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))
    df_gcp = pd.DataFrame(columns=["Video Id", "Phone Name", "GCP Score", "GCP Magnitude"])
    for index in data.index.values:
        transcript = data.loc[index]["text_reduced"]
        phone_name = data.loc[index]["phone_name"]
        video_id = data.loc[index]["video_id"]
        texts = " ".join(transcript)
        document = language_v1.Document(content=texts, type=language_v1.Document.Type.PLAIN_TEXT)
        sentiment = client.analyze_sentiment(
            request={"document": document}
        ).document_sentiment
        new_row = pd.DataFrame(
            {'Video Id': video_id, 'Phone Name': phone_name, 'GCP Score': sentiment.score,
             'GCP Magnitude': sentiment.magnitude},
            index=[0])
        print(new_row)
        df_gcp = pd.concat([new_row, df_gcp.loc[:]]).reset_index(drop=True)
    print(df_gcp)
    # insert_gcp_to_mongo(df_gcp)
    # print(df_row)
    # df_gcp = pd.concat([df_final, df_row], ignore_index=True)
    # print(df2)
    print("gcp completed")
    print(df_gcp)
    return df_gcp


def get_spacy_results(data):
    print("getting spacy results")
    # spacy.cli.download("en_core_web_sm")
    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe('spacytextblob')
    df_spacy = pd.DataFrame(columns=["Video Id", "Phone Name", "Spacy Label", "Spacy Score"])
    for index in data.index.values:
        transcript = data.loc[index]["text_reduced"]
        phone_name = data.loc[index]["phone_name"]
        video_id = data.loc[index]["video_id"]
        texts = " ".join(transcript)

        doc = nlp(texts)
        sentiment = doc._.blob.polarity
        sentiment = round(sentiment, 2)
        print("sentiment is")
        print(sentiment)
        if sentiment > 0:
            label = "Positive"
        elif sentiment == 0:
            label = "Neutral"
        else:
            label = "Negative"

        positive_words = []
        negative_words = []
        df_row = pd.DataFrame()

        for x in doc._.blob.sentiment_assessments.assessments:
            if x[1] > 0:
                positive_words.append(x[0][0])
            elif x[1] < 0:
                negative_words.append(x[0][0])
            else:
                pass

        # total_pos.append(', '.join(set(positive_words)))
        # total_neg.append(', '.join(set(negative_words)))

        new_row = pd.DataFrame(
            {'Video Id': video_id, 'Phone Name': phone_name, 'Spacy Label': label, 'Spacy Score': sentiment},
            index=[0])
        print(new_row)

        df_spacy = pd.concat([new_row, df_spacy.loc[:]]).reset_index(drop=True)
    print("spacy completed")
    print(df_spacy)
    return df_spacy


def get_roberta_results(data):
    print("getting roberta results")

    df_roberta = pd.DataFrame(columns=["Video Id", "Phone Name", "Roberta Neg", "Roberta Neu", "Roberta Pos"])
    for index in data.index.values:
        transcript = data.loc[index]["text_reduced"]
        phone_name = data.loc[index]["phone_name"]
        video_id = data.loc[index]["video_id"]
        try:

            task = 'sentiment'
            MODEL = f"cardiffnlp/twitter-roberta-base-{task}"

            tokenizer = AutoTokenizer.from_pretrained(MODEL)
            model = AutoModelForSequenceClassification.from_pretrained(MODEL)
            encoded_text = tokenizer(transcript, return_tensors='pt', padding='max_length', truncation=True, max_length=100)
            output = model(**encoded_text)
            scores = output[0][0].detach().numpy()
            scores = softmax(scores)

            scores_dict = {
                'roberta_neg': scores[0],
                'roberta_neu': scores[1],
                'roberta_pos': scores[2],
            }

        except Exception as e:
            print("Error occurred in roberta")
            scores[0] = 0
            scores[1] = 0
            scores[2] = 0

        finally:
            new_row = pd.DataFrame(
                {'Video Id': video_id, 'Phone Name': phone_name, 'Roberta Neg': scores[0], 'Roberta Neu': scores[1],
                 'Roberta Pos': scores[2]},
                index=[0])
            df_roberta = pd.concat([new_row, df_roberta.loc[:]]).reset_index(drop=True)
            print(new_row)
    print(df_roberta)
    print("roberta completed")
    return df_roberta


def get_siebert_results(data):
    print("getting siebert results")
    df_siebert = pd.DataFrame(columns=["Video Id", "Phone Name", "Siebert Label", "Siebert Score"])

    for index in data.index.values:
        transcript = data.loc[index]["text_reduced"]
        phone_name = data.loc[index]["phone_name"]
        video_id = data.loc[index]["video_id"]

        try:

            sentiment_analysis = pipeline("sentiment-analysis", model="siebert/sentiment-roberta-large-english")
            label = sentiment_analysis(transcript)[0]['label']
            score = sentiment_analysis(transcript)[0]['score']

        except Exception as e:
            print("Error occured in siebert")
            label = "None"
            score = 0
        finally:
            new_row = pd.DataFrame(
                {'Video Id': video_id, 'Phone Name': phone_name, 'Siebert Label': label, 'Siebert Score': score},
                index=[0])
            print(new_row)
            df_siebert = pd.concat([new_row, df_siebert.loc[:]]).reset_index(drop=True)
    print(df_siebert)
    print("siebert completed")
    return df_siebert


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
        data["text_reduced"] = texts_reduced
        data_subset = data[['video_id', 'phone_name', 'text_reduced']]
        return data_subset
    except Exception as e:
        print(e)
    print("youtube data loaded successfully")


if __name__ == '__main__':
    data = get_youtube_data_mongo()
    # print(data)
    gcp = get_gcp_results(data)
    spcy = get_spacy_results(data)
    roberta = get_roberta_results(data)
    siebert = get_siebert_results(data)
    insert_all_sentiments_mongo(gcp, spcy, roberta, siebert)
    #insert_all_sentiments_mongo(gcp, spcy, siebert)
