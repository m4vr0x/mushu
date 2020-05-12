#!/usr/bin/env python

import sys
import os
import fnmatch
import re
import pymongo
import logging

import main

def list_episode(dir_path, db_collection, db_client, db_name):

    mesg = ("===== Connecting Database"); logging.info(mesg)

    try:
        db_client.server_info()
    except pymongo.errors.ServerSelectionTimeoutError as err:
        mesg = (f'Impossible to connect to the database:\n{db_client}')
        logging.error(mesg); sys.exit("!Error! "+mesg)

    db_client.drop_database(db_name)

    if not os.path.isdir(dir_path):
        mesg = (f'The specified base directory does not exist:\n\t{dir_path}')
        logging.error(mesg); sys.exit("!Error! "+mesg)

    mesg = ("===== Listing files"); logging.info(mesg)

    for file_path, dir_name, file in os.walk(dir_path):

        if re.search('^.+Kaamelott.+$', file_path): continue

        for file_name in file:
            if fnmatch.fnmatch(file_name, '[!._]*') and file_name.endswith(('.mkv', '.avi')):

                mesg = (f'File found: {file_name}'); logging.info(mesg)

                path_match = re.search('^'+dir_path+'\/*(.+)\/[Ss](.+)$', file_path)
                if path_match:
                    path_show_name = path_match.group(1)
                    path_season_number = path_match.group(2)
                else:
                    mesg = (f'Impossible to parse file path:\n\t{file_path}')
                    logging.error(mesg); sys.exit("!Error! "+mesg)

                file_match = re.search('^(.+).[Ss]([0-9][0-9])\.*[Ee]([0-9]*[0-9][0-9]).+$', file_name)
                if file_match:
                    file_show_name = file_match.group(1)
                    file_season_number = file_match.group(2)
                    file_episode_number = file_match.group(3)
                else:
                    mesg = (f'Impossible to parse file name:\n\t{file_name}')
                    logging.error(mesg); sys.exit("!Error! "+mesg)

                media_dict = { "name": file_name, "full_path": (f"{file_path}/{file_name}"), "path": file_path, "base_dir": dir_path, "tv_show": path_show_name, "season_number": file_season_number, "episode_number": file_episode_number }

                mesg = 'media_dict content:'
                for key, value in media_dict.items(): mesg += (f'\n\t{key}= {value}')
                logging.debug(mesg)

                db_collection.insert_one(media_dict)

if __name__ == "__main__":
    list_episode(dir_path, db_collection)
