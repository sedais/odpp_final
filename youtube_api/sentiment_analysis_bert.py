import transformers
from transformers import BertModel, BertTokenizer, AdamW, get_linear_schedule_with_warmup
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
from api_search import search_by_query

import re
import torch
import numpy

PRE_TRAINED_MODEL_NAME = "bert-base-cased"


def instantiate_model():
    tokenizer = AutoTokenizer.from_pretrained


def main():
    query = "iPhone 11 change battery"
    types = ["channel", "playList", "video"]
    # for t in types:
    #    search_by_query(query, t)
    df = search_by_query(query, "video")

    classifier = pipeline("sentiment-analysis", model="finiteautomata/bertweet-base-sentiment-analysis")
    data = df['transcript']
    sentiments = []
    scores = []

    for item in data:
        # print(item)
        # print(type(item)) # series
        pos_score, neg_score, neu_score = 0, 0, 0
        pos_counter, neg_counter, neu_counter = 0, 0, 0
        total_pos, total_neg, total_neu = 0, 0, 0

        # if item is empty
        if not item:
            sentiments.append("None")
            scores.append(0)
        else:
            for sentence in item:
                output = classifier(sentence)
                # print(sentence)
                for out in output:
                    # print(out)
                    if out['label'] == 'POS':
                        pos_score += out['score']
                        pos_counter += 1
                    if out['label'] == 'NEG':
                        neg_score += out['score']
                        neg_counter += 1
                    if out['label'] == 'NEU':
                        neu_score += out['score']
                        neu_counter += 1

            total_pos = pos_score / pos_counter
            total_neg = neg_score / neg_counter
            total_neu = neu_score / neu_counter
            print(total_pos)
            print(total_neg)
            print(total_neu)

            overall_score = max(total_pos, total_neg, total_neu)
            print("overall score")
            print(overall_score)
            if overall_score == total_pos:
                print("pos")
                sentiments.append("positive")
            if overall_score == total_neg:
                sentiments.append("negative")
                print("neg")
            if overall_score == total_neu:
                sentiments.append("neutral")
                print("neu")

            scores.append(overall_score)
            print(scores)
            print(sentiments)

    df['score'] = scores
    df['sentiment'] = sentiments

    print(df)
    # print(tabulate(df, headers='keys', tablefmt='fancy_grid'))


if __name__ == "__main__":
    main()
