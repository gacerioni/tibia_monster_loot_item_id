import os

mongodb_config = dict(
    mongodb_user = str(os.environ.get('TIBIA_API_MONGODB_USR')),
    mongodb_pwd = str(os.environ.get('TIBIA_API_MONGODB_PWD')),
    mongodb_cluster_conn_str = "cluster0.dkifc.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",
    mongodb_tibia_db = "tibia",
    mongodb_tibia_item_id_collection = "item_and_id")
