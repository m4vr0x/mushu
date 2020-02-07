#!/usr/bin/env python

import sys
import os
import fnmatch
import re
import pymongo

def list_episode(dir_path, db_collection, db_client, db_name):

    try:
        db_client.server_info()
    except pymongo.errors.ServerSelectionTimeoutError as err:
        error_mesg = (f'!Error! Impossible to connect to the database:\n{db_client}')
        sys.exit(error_mesg)

    db_client.drop_database(db_name)

    if not os.path.isdir(dir_path):
        error_mesg = (f'!Error! The specified base directory does not exist:\n\t{dir_path}')
        sys.exit(error_mesg)

    for file_path, dir_name, file in os.walk(dir_path):

        if re.search('^.+Kaamelott.+$', file_path): continue

        # print(f'\nfile_path:{file_path}\ndir_name:{dir_name}\nfile:{file}')

        for file_name in file:
            # if re.search('^.+Kaamelott.+$', file_name): continue

            if fnmatch.fnmatch(file_name, '[!._]*') and file_name.endswith(('.mkv', '.avi')):

                path_match = re.search('^'+dir_path+'\/(.+)\/[Ss](.+)$', file_path)
                if path_match:
                    path_show_name = path_match.group(1)
                    path_season_number = path_match.group(2)
                else:
                    error_mesg = (f'!Error! Impossible to parse file path:\n\t{file_path}')
                    sys.exit(error_mesg)

                file_match = re.search('^(.+).[Ss]([0-9][0-9])\.*[Ee]([0-9]*[0-9][0-9]).+$', file_name)
                if file_match:
                    file_show_name = file_match.group(1)
                    file_season_number = file_match.group(2)
                    file_episode_number = file_match.group(3)
                else:
                    error_mesg = (f'!Error! Impossible to parse file name:\n\t{file_name}')
                    sys.exit(error_mesg)

                media_dict = { "name": file_name, "full_path": (f"{file_path}/{file_name}"), "path": file_path, "base_dir": dir_path, "tv_show": path_show_name, "season_number": file_season_number, "episode_number": file_episode_number }

                db_collection.insert_one(media_dict)

if __name__ == "__main__":
    list_episode(dir_path, db_collection)
