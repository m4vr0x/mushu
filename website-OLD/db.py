# from app import app
import pymongo
import pandas

db_host = "localhost"
db_port = "27017"
db_name = "media_scan-3_10"
collection_name = "files"

db_client = pymongo.MongoClient("mongodb://"+db_host+":"+db_port+"/",serverSelectionTimeoutMS=3000)
db_collection = (db_client[db_name])[collection_name]

show_list = list_series(db_collection)
return show_list

def test_db_acces(db_collection):

    try:
        db_client.server_info()
    except pymongo.errors.ServerSelectionTimeoutError as err:
        error_mesg = (f'!Error! Impossible to connect to the database:\n{db_client}')
        sys.exit(error_mesg)

def list_series(db_collection):
    show_list = db_collection.distinct("tv_show")
    return show_list
