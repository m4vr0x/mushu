#!/usr/bin/env python

import argparse
import pymongo
import sys

import logging
import time

import initiate_db
import analyse_media

dir_path = ""
collection_name = "files"

def parse_options():
    parser = argparse.ArgumentParser(description="Scan media file library")
    parser.add_argument('-l', "--library",
                        action="store", dest='dir_path', default="",
                        help='Path of library directory to scan')
    parser.add_argument('-d', "--database",
                        action="store", dest='db_name', default="media_scan",
                        help='Name of the database')
    parser.add_argument('-s', "--server",
                        action="store", dest='db_host', default="localhost",
                        help='Hostname/ip of the database')
    parser.add_argument('-p', "--port",
                        action="store", dest='db_port', default="27017",
                        help='Port of the database')
    args = parser.parse_args()
    return args.dir_path, args.db_name, args.db_host, args.db_port;

def main():

    logging.basicConfig(filename='media_scan.log', filemode='w', format='%(asctime)s %(name)s -%(levelname)s- %(message)s', level=logging.DEBUG)

    mesg = ("Calling parse_options")
    logging.debug(mesg)
    # print("+DEBUG+ "+mesg)
    dir_path, db_name, db_host, db_port = parse_options()

    # db_client = pymongo.MongoClient("mongodb://"+db_host+":"+db_port+"/",serverSelectionTimeoutMS=3000)
    db_client = pymongo.MongoClient(f'mongodb://{db_host}:{db_port}/',serverSelectionTimeoutMS=3000)
    db_collection = (db_client[db_name])[collection_name]
    mesg = (f'\n\tdir_path = {dir_path}\n\tdb_host = {db_host}\n\tdb_port = {db_port}')
    logging.debug(mesg)

    mesg = ("Calling initiate_db.list_episode")
    logging.debug(mesg)
    # print("+DEBUG+ "+mesg)
    initiate_db.list_episode(dir_path, db_collection, db_client, db_name)

    mesg = ("Calling analyse_media.media_info")
    logging.debug(mesg)
    # print("+DEBUG+ "+mesg)
    analyse_media.media_info(db_collection)


if __name__ == "__main__":
    main()
