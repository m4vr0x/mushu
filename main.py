#!/usr/bin/env python

import sys
import os
import fnmatch
import re

## Check Python version

if not sys.version_info.major == 3 and sys.version_info.minor >= 6:
    print("This script requires Python 3.5 or higher!")
    print("You are using Python {}.{}.".format(sys.version_info.major, sys.version_info.minor))
    sys.exit(1)

class Episode:
  def __init__(self, file, path):
    self.file = file
    self.path = path
    # self.toto = toto

episode_list = []

## Walking the directory tree and populating
def dir_parsing(dir_path):
    for dirpath, dirnames, files in os.walk(dir_path):
        file_path = dirpath
        for file_name in files:
            if fnmatch.fnmatch(file_name, '[!._]*') and file_name.endswith(('.mkv', '.avi')):
                    episode_list.append(file_name)
                    # print(f'PATH={file_path}=\nNAME={file_name}=\n')
                    file_name = Episode(file_name, file_path)
                    print(f'NAME=|{file_name.file}|\nPATH=|{file_name.path}|\n')


def main():
    dir_parsing('/Users/vinz/Documents/Media_scan/TV-SHOWS')
    # print(toto.file)
    # for i in episode_list:
    #     print(i)
    #     print(i.path)

if __name__ == "__main__":
    main()
