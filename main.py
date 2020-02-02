#!/usr/bin/env python

import pymongo

import initiate_db

dir_path = '/Users/vinz/Documents/Media_scan/TV-SHOWS-Fake'
# dir_path = '/Users/vinz/Documents/Media_scan/TV-SHOWS-Real'

db_client = pymongo.MongoClient("mongodb://localhost:27017/")
db_name = db_client["media_scan"]
db_collection = db_name["files"]

def main():

    # pass
    for x in db_collection.find():
      print(x)


if __name__ == "__main__":
    initiate_db.list_episode(dir_path, db_collection)
    main()
