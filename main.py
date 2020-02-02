#!/usr/bin/env python

import pymongo

import initiate_db
import analyse_media

# dir_path = '/Users/vinz/Documents/Media_scan/TV-SHOWS-Fake'
dir_path = '/Users/vinz/Documents/Media_scan/TV-SHOWS-Real'

db_client = pymongo.MongoClient("mongodb://localhost:27017/")
db_name = db_client["media_scan"]
db_collection = db_name["files"]

def main():

    # # DEBUG
    # pass
    # # DEBUG

    initiate_db.list_episode(dir_path, db_collection)

    # # DEBUG
    # for x in db_collection.find():
    #   print(x)
    # # DEBUG

    for media_path in db_collection.distinct("full_path"):
        analyse_media.media_info(media_path)


if __name__ == "__main__":
    main()
