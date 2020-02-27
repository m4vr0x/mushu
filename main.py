#!/usr/bin/env python

import argparse
import pymongo
import sys

import initiate_db
import analyse_media

dir_path = ""

db_name = "media_scan"
collection_name = "files"

def parse_options():
    parser = argparse.ArgumentParser(description="Scan media file library")
    parser.add_argument('-d', "--directory",
                        action="store", dest='dir_path', default="",
                        help='Path of library directory to scan')
    parser.add_argument('-s', "--server",
                        action="store", dest='db_host', default="localhost",
                        help='Hostname/ip of the database')
    parser.add_argument('-p', "--port",
                        action="store", dest='db_port', default="27017",
                        help='Port of the database')
    args = parser.parse_args()
    return args.dir_path, args.db_host, args.db_port;

def main():

    dir_path, db_host, db_port = parse_options()

    db_client = pymongo.MongoClient("mongodb://"+db_host+":"+db_port+"/",serverSelectionTimeoutMS=3)
    db_collection = (db_client[db_name])[collection_name]

    initiate_db.list_episode(dir_path, db_collection, db_client, db_name)

    print(f'\n===\n Analyse files\n===\n')
    analyse_media.media_info(db_collection)


if __name__ == "__main__":
    main()
