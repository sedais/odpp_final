import pymongo
from ifixit.web_scraper_ifixit import *
import logging

if __name__ == '__main__':
    client = pymongo.MongoClient(
        "mongodb+srv://Python:hQTMon51YyXJjzLT@odpp.proeq78.mongodb.net/?retryWrites=true&w=majority")
    print(client.list_database_names())
    db = client.PhoneDB
    print(db.list_collection_names())

    col = db['Phones']
    ifixtit_col = db['ifixit']

    df_ifixit = get_the_content()
    dict_ifixit = df_ifixit.to_dict('records')
    ifixtit_col.insert_many(dict_ifixit)

    doc = ifixtit_col.count_documents({})
    print(doc)
    client.close()







