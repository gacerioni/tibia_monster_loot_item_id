import re
from utils import config
from pymongo import MongoClient

MONGO_USR = config.mongodb_config['mongodb_user']
MONGO_PWD = config.mongodb_config['mongodb_pwd']
MONGO_CONNSTR = config.mongodb_config['mongodb_cluster_conn_str']
MONGO_TIBIA_DB = config.mongodb_config['mongodb_tibia_db']
MONGO_TIBIA_ITEMID_COLLECTION = config.mongodb_config['mongodb_tibia_item_id_collection']


def get_mongodb_tibia_itemid_collection():
    client = MongoClient("mongodb+srv://{0}:{1}@{2}".format(MONGO_USR, MONGO_PWD, MONGO_CONNSTR))

    tibia_db = client[MONGO_TIBIA_DB]
    tibia_item_and_id_collection = tibia_db[MONGO_TIBIA_ITEMID_COLLECTION]

    return tibia_item_and_id_collection

def get_all_tibia_itemid_from_collection():
    itemid_collection_list = []
    itemid_collection = get_mongodb_tibia_itemid_collection()

    collection_result = itemid_collection.find({}, {'_id': False})

    for item_id in collection_result:
        itemid_collection_list.append(item_id)

    return itemid_collection_list

if __name__ == '__main__':
    print(get_all_tibia_itemid_from_collection())
