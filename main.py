#!/usr/bin/env python

import pymongo
import sys

import initiate_db
import analyse_media

# dir_path = '/Users/vinz/Documents/Media_scan/TV-SHOWS-Real'
dir_path = '/Volumes/GoogleDrive/My Drive/Hulk/TV Shows'

db_name = "media_scan"
collection_name = "files"

db_client = pymongo.MongoClient("mongodb://localhost:27017/",serverSelectionTimeoutMS=3)
db_collection = (db_client[db_name])[collection_name]

def main():

    initiate_db.list_episode(dir_path, db_collection, db_client, db_name)

    analyse_media.media_info(db_collection)


if __name__ == "__main__":
    main()
