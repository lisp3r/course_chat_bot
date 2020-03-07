from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from yaml import load, Loader


DBCONFIG = 'database.yml'

class DatabaseUnavaliable(ServerSelectionTimeoutError):
    pass

class db_info():
    def __init__(self, db_config):
        with open(db_config, 'r') as cfg_file:
            cfg_data = load(cfg_file, Loader=Loader)
        self.url = cfg_data['database']['url']
        self.port = cfg_data['database']['port']
        self.name = cfg_data['database']['name']
        # self.collections = cfg_data['database']['collections']

    def mongo_url(self):
        return f"mongodb://{self.url}:{self.port}/"

def save_to_mongo(doc):
    assert isinstance(doc, dict)

    db = db_info(DBCONFIG)
    client = MongoClient(db.mongo_url(), serverSelectionTimeoutMS = 2000)
    try:
        client.server_info()
    except ServerSelectionTimeoutError:
        raise DatabaseUnavaliable
    bot_database = client[db.name]
    log_collection = bot_database['log']
    return log_collection.insert_one(doc)


# bot_db = client[db.name]
# info_collection = bot_db['info']
# info_collection.insert_one({'user': 'lisp3r'})

# print(client.list_database_names())
