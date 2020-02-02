#!/usr/bin/env python

import sys
import os
import fnmatch
import re
import pymongo

def list_episode(dir_path, db_collection):
    for paths, dirnames, files in os.walk(dir_path):
        file_path = paths

        for file_name in files:
            if fnmatch.fnmatch(file_name, '[!._]*') and file_name.endswith(('.mkv', '.avi')):

                path_match = re.search('^'+dir_path+'\/(.+)\/S(.+)$', file_path)
                if path_match:
                    path_show_name = path_match.group(1)
                    path_season_number = path_match.group(2)

                file_match = re.search('^(.+).S([0-9][0-9]).E([0-9][0-9]).+$', file_name)
                if file_match:
                    file_show_name = file_match.group(1)
                    file_season_number = file_match.group(2)
                    file_episode_number = file_match.group(3)

                # # # DEBUG
                # print(f'NAME |{file_name}|\n \
                #         FULL_PATH |{file_path}/{file_name}|\n \
                #         PATH |{file_path}|\n \
                #         BASE_DIR |{dir_path}|\n \
                #         PATH_TV_SHOW |{path_show_name}|\n \
                #         FILE_TV_SHOW |{file_show_name}|\n \
                #         PATH_SEASON |{path_season_number}|\n \
                #         FILE_SEASON |{file_season_number}|\n \
                #         FILE_EPISODE |{file_episode_number}|\n \
                #         ')
                # # # DEBUG

                media_dict = { "name": file_name, "full_path": (f"{file_path}/{file_name}"), "path": file_path, "base_dir": dir_path, "tv_show": path_show_name, "season_number": file_season_number, "episode_number": file_episode_number }

                # # # DEBUG
                # print(media_dict)
                # # # DEBUG
                
                db_collection.insert_one(media_dict)


if __name__ == "__main__":
    list_episode(dir_path, db_collection)
