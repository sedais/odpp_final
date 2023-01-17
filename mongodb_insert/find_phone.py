import pymongo


def main():
    client = pymongo.MongoClient(
        "mongodb+srv://Python:hQTMon51YyXJjzLT@odpp.proeq78.mongodb.net/?retryWrites=true&w=majority")
    db = client.PhoneDB
    collection = db.Phones

    phone_name = "Nokia 3210"
    phone = collection.find_one({"name":phone_name})

    if f"Removable {phone['battery_type']} battery" in phone["specifications"]:
        print("Battery can be removed")
    else:
        print("Battery can not be removed")

    client.close()


if __name__ == '__main__':
    main()
