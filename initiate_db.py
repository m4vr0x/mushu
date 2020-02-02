#!/usr/bin/env python

import sys
import os
import fnmatch
import re
import pymongo

def list_episode(dir_path, db_collection):
    if not os.path.isdir(dir_path):
        error_mesg = (f'!Error! The specified base directory does not exist:\n\t{dir_path}')
        sys.exit(error_mesg)

    for paths, dirnames, files in os.walk(dir_path):
        file_path = paths

        for file_name in files:
            if fnmatch.fnmatch(file_name, '[!._]*') and file_name.endswith(('.mkv', '.avi')):

                # # DEBUG
                # print(f'\nNAME |{file_name}|')
                # print(f'\tFULL_PATH |{file_path}/{file_name}|')
                # print(f'\tPATH |{file_path}|')
                # print(f'\tBASE_DIR |{dir_path}|')
                # # DEBUG

                path_match = re.search('^'+dir_path+'\/(.+)\/[Ss](.+)$', file_path)
                if path_match:
                    path_show_name = path_match.group(1)
                    path_season_number = path_match.group(2)
                else:
                    error_mesg = (f'!Error! Impossible to parse:\n\t{file_path}')
                    sys.exit(error_mesg)

                # # DEBUG
                # print(f'\tPATH_TV_SHOW |{path_show_name}|')
                # print(f'\tPATH_SEASON |{path_season_number}|')
                # # DEBUG

                file_match = re.search('^(.+).[Ss]([0-9][0-9])\.*[Ee]([0-9][0-9]).+$', file_name)
                if file_match:
                    file_show_name = file_match.group(1)
                    file_season_number = file_match.group(2)
                    file_episode_number = file_match.group(3)
                else:
                    error_mesg = (f'!Error! Impossible to parse:\n\t{file_name}')
                    sys.exit(error_mesg)

                # # DEBUG
                # print(f'\tFILE_TV_SHOW |{file_show_name}|')
                # print(f'\tFILE_SEASON |{file_season_number}|')
                # print(f'\tFILE_EPISODE |{file_episode_number}|')
                # # DEBUG

                media_dict = { "name": file_name, "full_path": (f"{file_path}/{file_name}"), "path": file_path, "base_dir": dir_path, "tv_show": path_show_name, "season_number": file_season_number, "episode_number": file_episode_number }

                # # DEBUG
                # print(media_dict)
                # # DEBUG

                db_collection.insert_one(media_dict)


if __name__ == "__main__":
    list_episode(dir_path, db_collection)
