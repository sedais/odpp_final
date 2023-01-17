from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re

from tabulate import tabulate


def get_the_content():
    # Open up local html file (downloaded from the web)
    with open("Repairability_Scores_iFixit.html", "r") as f:
        soup = BeautifulSoup(f, "html.parser")
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
                facts.append("positive: " + str(pos.string))
            for neut in detail.find_all("li", class_="device-detail neutral"):
                facts.append("neutral: " + str(neut.string))
            for neg in detail.find_all("li", class_="device-detail minus"):
                facts.append("negative: " + str(neg.string))

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
    return df_ifixit_phones


if __name__ == '__main__':
    # Read devices json
    df_devices = pd.read_json("../youtube_api/devices.json")
    # print(type(df_devices))
    # print(df_devices.head())
    # print(list(df_devices.columns))
    # print(df_devices['RECORDS'].to_dict())

    records = df_devices['RECORDS']

    # Read csv
    df_phones = pd.read_csv('../youtube_api/phone_dataset.csv', on_bad_lines='skip')
    # print(df_phones.head())
    # print(df_phones.columns)
    battery = df_phones[["brand", "model", "battery"]]
    print(battery.head())
    # battery["name"] = battery['brand'] + " " + battery["model"]
    # print(battery.head())

    # Get the content and parse it to a dataframe
    df_ifixit = get_the_content()
    print(tabulate(df_ifixit, headers='keys', tablefmt='psql'))
    # print(df_ifixit.head())

    print(df_ifixit['model'])
    print("---------------")
    print(battery['model'])

    df_merged = pd.merge(df_ifixit, battery, on='model', how='inner')
    # print(df_merged)
    print(tabulate(df_merged, headers='keys', tablefmt='psql'))