import re
import config
import urllib.request
from bs4 import BeautifulSoup
from html_table_parser import HTMLTableParser
from pymongo import MongoClient


def mongodb_client_connection(user, pwd, connstr):
    client = MongoClient("mongodb+srv://{0}:{1}@{2}".format(user, pwd, connstr))

    return client

def mongodb_inject_item_id(mongodb_collection):
    raw_payload = get_tibia_id_dict()
    mongodb_document_list = []

    for item in raw_payload:
        temp_dict = {}
        temp_dict["item_name"] = item.replace(".", "#")
        temp_dict["item_id"] = raw_payload[item]
        #temp_dict[item.replace(".", "#")] = raw_payload[item]

        mongodb_document_list.append(temp_dict)
    
    mongodb_collection.insert_many(mongodb_document_list)

def mongodb_clean_item_id_collection(mongodb_collection):
    
    mongodb_collection.delete_many({})


def url_get_contents(url):
    """ Opens a website and read its binary contents (HTTP Response Body) """
    req = urllib.request.Request(url=url)
    f = urllib.request.urlopen(req)
    return f.read()


def get_tibia_id_dict():
    url = 'https://tibia.fandom.com/wiki/Item_IDs'
    xhtml = url_get_contents(url).decode('utf-8')

    p = HTMLTableParser()
    p.feed(xhtml)

    item_dict_final = {}
    for item in p.tables[0][1:]:
        item_dict_final[item[0]] = item[1]

    return (item_dict_final)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
   
   # 1-) Creating the MongoDB client, db, connection

    mongo_usr = config.mongodb_config['mongodb_user']
    mongo_pwd = config.mongodb_config['mongodb_pwd']
    mongo_connstr = config.mongodb_config['mongodb_cluster_conn_str']
    mongo_db =  config.mongodb_config['mongodb_tibia_db']
    mongo_collection = config.mongodb_config['mongodb_tibia_item_id_collection']

    client = mongodb_client_connection(mongo_usr, mongo_pwd, mongo_connstr)
    tibia_db = client[mongo_db]
    tibia_item_and_id_collection = tibia_db[mongo_collection]

    # 2-) Cleaning last Collection, in case anything changes
    mongodb_clean_item_id_collection(tibia_item_and_id_collection)

    # 3-) Loading the new Collection
    mongodb_inject_item_id(tibia_item_and_id_collection)

    print(tibia_item_and_id_collection.find_one({"item_name" : "Platinum Coin"}))

