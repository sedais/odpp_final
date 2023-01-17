from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from urllib.request import urlopen
from tabulate import tabulate


def clean_ifixit_data(df):
    df['score'] = df['score'].astype('int')

    # Replacing "'" read as â€™
    df['fact1'] = df['fact1'].str.replace('â€™', ' i')
    df['fact2'] = df['fact2'].str.replace('â€™', ' i')
    df['fact3'] = df['fact3'].str.replace('â€™', ' i')

    # Adding missing information due to <em> tags
    df.loc[
        15, 'fact3'] = "Glass on front and back doubles the likelihood of drop damage—and if the back glass breaks, you'll be removing every component and replacing the entire chassis."
    df.loc[24, 'fact2'] = "Replacing the battery—or rather, batteries—requires near-total disassembly."
    df.loc[
        27, 'fact3'] = "Glass on front and back doubles the likelihood of drop damage—and if the back glass breaks, you'll be removing every component and replacing the entire chassis."
    df.loc[
        40, 'fact3'] = "Glass on front and back doubles the likelihood of drop damage—and if the back glass breaks, you'll be removing every component and replacing the entire chassis."
    df.loc[
        40, 'fact3'] = "Removing the rear case to access the motherboard and other internals requires a lot of careful prying and guitar-picking."

    # Fixing brand, model inconsistency with Apple phones
    df.loc[df['brand'] == "iPhone", 'model'] = "iPhone " + df['model']
    df.loc[df["brand"] == "iPhone", "brand"] = "Apple"

    return df


def get_me():
    return "is it working?"


def get_content_from_mongo():
    print("in get content from mongo")
    try:
        client = MongoClient(
            "mongodb+srv://odpp_user:Uu5VxTud3tkbklwT@atlascluster.aqrdbga.mongodb.net/?retryWrites=true&w=majority")

        print(client.list_database_names())
        db = client.ifixit_db
        collection = db.phones
        data = pd.DataFrame(collection.find())
        print(data.head())
    except Exception as e:
        print(e)
    return data


def insert_to_mongo(dict):
    try:
        client = MongoClient(
            "mongodb+srv://odpp_user:Uu5VxTud3tkbklwT@atlascluster.aqrdbga.mongodb.net/?retryWrites=true&w=majority")
        print("Available databases in mongo db: ")
        print(client.list_database_names())
        db = client.ifixit_db
        collection = db.phones
        print(collection)

        phone_names = df_ifixit["brand"] + " " + df_ifixit["model"]
        print(type(phone_names.values))
        print(list(phone_names))

        print("Deleting the existing collections...")
        collection.delete_many({})
        print("Deleted collections.")

        print("Inserting ifixit data into collections...")
        collection.insert_many(dict)
        print("Inserted.")

    except Exception as e:
        print(e)
    else:
        print("Test connection is successful")


def get_the_content():
    # Open up local html file (downloaded from the web)
    # with open("Smartphone_Repairability_Scores_iFixit_updated.html", "r") as f:
    #     soup = BeautifulSoup(f, "html.parser")

    # Or with url from the web
    url = "https://www.ifixit.com/smartphone-repairability?sort=date"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    df_ifixit_phones = pd.DataFrame(columns=['brand', 'model', 'year', 'score', 'fact1', 'fact2', 'fact3'])

    brands, models, years, scores, facts = ([] for _ in range(5))

    for div in soup.find_all("div", class_="row"):
        for item in div.find_all("div", class_="cell image-container"):
            for a in item.find_all("img"):
                phone_name = re.search(r'alt=(.*?)class', str(a)).group(1)
                phone_name = phone_name.replace('"', "")
                brands.append(phone_name.split()[0])
                # names.append(phone_name)
        for sub0 in div.find_all("h3"):
            scores.append(sub0.string)
        for sub in div.find_all("div", class_="cell device-name"):
            for sub2 in sub.find_all("span", class_="selected"):
                models.append(sub2.string)
            for sub3 in sub.find_all("span", class_="date"):
                years.append(sub3.string)
        for detail in div.find_all("div", class_="cell hidden-mobile"):
            for pos in detail.find_all("li", class_="device-detail plus"):
                facts.append(str(pos.string))
            for neut in detail.find_all("li", class_="device-detail neutral"):
                facts.append(str(neut.string))
            for neg in detail.find_all("li", class_="device-detail minus"):
                facts.append(str(neg.string))

    # df_ifixit_phones['name'] = names
    df_ifixit_phones['brand'] = brands
    df_ifixit_phones['model'] = models

    df_ifixit_phones['year'] = years
    fact1 = facts[::3]
    fact2 = facts[1::3]
    fact3 = facts[2::3]
    # print(len(fact1))
    # print(len(facts))

    df_ifixit_phones['fact1'] = fact1
    df_ifixit_phones['fact2'] = fact2
    df_ifixit_phones['fact3'] = fact3

    df_ifixit_phones['score'] = scores
    # df_ifixit_phones['brand'] = brands

    df_ifixit_phones = clean_ifixit_data(df_ifixit_phones)

    return df_ifixit_phones


if __name__ == '__main__':

    # Get the content
    df_ifixit = get_the_content()
    print(tabulate(df_ifixit, headers='keys', tablefmt='psql'))

    # dict_fixit = df_ifixit.to_dict('records')
    # insert_to_mongo(dict_fixit)

    #df_mongo = get_content_from_mongo()
    #print(tabulate(df_mongo, headers='keys', tablefmt='psql'))


