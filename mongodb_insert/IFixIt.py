import pymongo
from save_input import load_save


def main():
    client = pymongo.MongoClient(
        "mongodb+srv://Python:hQTMon51YyXJjzLT@odpp.proeq78.mongodb.net/?retryWrites=true&w=majority")
    db = client.PhoneDB
    collection = db.ifixit
    input = load_save()
    if input is not None:
        parts = input.split(" ")
        phone = collection.find_one({"brand": parts[0], "model": input.replace(parts[0], "").strip()})
        print(phone["score"])

    client.close()


if __name__ == '__main__':
    main()
