import pymongo
import json


def main():
    client = pymongo.MongoClient(
        "mongodb+srv://Python:hQTMon51YyXJjzLT@odpp.proeq78.mongodb.net/?retryWrites=true&w=majority")
    db = client.PhoneDB
    collection = db.Phones

    with open('devices.json') as file:
        file_data = json.load(file)

    collection.insert_many(file_data["RECORDS"])
    client.close()


if __name__ == '__main__':
    main()
