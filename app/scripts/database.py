import logging
import pymongo
import os
import sys
import re
import fnmatch

def setup_db_client():
    db_client = pymongo.MongoClient("db", 27017, serverSelectionTimeoutMS=5000)
    logging.info("Initialising database and collection...")
    database = db_client["mushu"]
    collection = database["files"]
    return db_client, database, collection

def test_db_connection(db_client):
    logging.info("Testing database connection...")
    try:
        db_client.server_info()
        msg = "Succefully connected to MongoDB"
        logging.info(msg)
        return msg
    except pymongo.errors.ServerSelectionTimeoutError as e:
        msg = (f'Connection try timed out: {e}')
        logging.critical(msg)
        return msg
    except Exception:
        raise

def populate_db(dir_path, db_client, collection):
    db_list = db_client.list_database_names()
    if "mushu" in db_list:
        msg = "Database already exists and will be cleaned"
        logging.warning(msg)
        db_client.drop_database("mushu")

    logging.info("Listing files...")
    for file_path, dir_name, file in os.walk(dir_path):
        if re.search('^.+Kaamelott.+$', file_path): continue

        for file_name in file:
            if fnmatch.fnmatch(file_name, '[!._]*') and file_name.endswith(('.mkv', '.avi')):
                mesg = (f'File found: {file_name}'); logging.info(mesg)
                path_match = re.search('^'+dir_path+'\/*(.+)\/[Ss](.+)$', file_path)

                if path_match:
                    path_show_name = path_match.group(1).replace(".", " ")
                    path_season_number = path_match.group(2)
                else:
                    mesg = (f'Impossible to parse file path: "{file_path}"')
                    logging.error(mesg)
                    raise OSError(mesg)

                file_match = re.search('^(.+).[Ss]([0-9][0-9])\.*[Ee]([0-9]*[0-9][0-9]).+$', file_name)

                if file_match:
                    file_show_name = file_match.group(1)
                    file_season_number = file_match.group(2)
                    file_episode_number = file_match.group(3)
                else:
                    mesg = (f'Impossible to parse file name: "{file_name}"')
                    logging.error(mesg)
                    raise OSError(mesg)

                media_dict = { "name": file_name, "full_path": (f"{file_path}/{file_name}"), "path": file_path, "base_dir": dir_path, "tv_show": path_show_name, "season_number": file_season_number, "episode_number": file_episode_number }
                mesg = 'media_dict content:'
                for key, value in media_dict.items(): mesg += (f'\n\t{key}: {value}')
                logging.debug(mesg)

                collection.insert_one(media_dict)

    series_list = []
    for show in collection.distinct("tv_show"):
        series_list.append(show)
    series_list = sorted(set(series_list), key=series_list.index)
    print(series_list)
    return series_list
