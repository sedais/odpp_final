from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import requests
from bs4 import BeautifulSoup
import sys
import os
import glob


def bert(filename):
    with open(filename, "r") as file:
        content = file.read()
        content += content.replace("\n", " ")

    # transcript = ""
    # for line in lines:
    #    transcript += line.replace("\n", " ")

    tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
    model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
    tokens = tokenizer.encode("This movie was very good", return_tensors='pt')
    result = model(tokens)
    return int(torch.argmax(result.logits)) + 1

    # results = []
    # for line in lines:
    #    tokens = tokenizer.encode(line, return_tensors='pt')
    #    result = model(tokens)
    #    results.append(int(torch.argmax(result.logits)) + 1)

    # print(sum(results)/len(results))


if __name__ == "__main__":
    # sys.argv.append("video_ids.txt")
    results = []
    dir = r"C:\Users\a881910\GitHub\ODPP\mongodb_insert\transcripts"
    for path in os.listdir(dir):
        results.append(bert(os.path.join(dir, path)))
    print(round(sum(results) / len(results), 2))
