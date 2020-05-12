#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import pymongo
from flask import *
import pandas
app = Flask(__name__)

db_host = "localhost"
db_port = "27017"
db_name = "media_scan-3_10"
collection_name = "files"

db_client = pymongo.MongoClient("mongodb://"+db_host+":"+db_port+"/",serverSelectionTimeoutMS=3000)
db_collection = (db_client[db_name])[collection_name]

def test_db_acces(db_collection):

    try:
        db_client.server_info()
    except pymongo.errors.ServerSelectionTimeoutError as err:
        error_mesg = (f'!Error! Impossible to connect to the database:\n{db_client}')
        sys.exit(error_mesg)

def main():

    print(f'\n===\n Initiate Database \n===\n')
    test_db_acces(db_collection)

    show_list = db_collection.distinct("tv_show")

    @app.route('/')
    def home_view():
        return render_template('home.html', SHOW_LIST=show_list, B=db_name)

    @app.route('/<serie_name>')
    def serie_view(serie_name):
        episodes = db_collection.find({ "tv_show" : serie_name })

        df = pandas.DataFrame(data = episodes)
        season_list = df.season_number.unique()

        data = ''

        for season in season_list:
            season_table = df[df['season_number'] == season]

            data += 'Season '+season+'<br/><br/>'
            data += season_table.to_html(index=False, justify="left", columns = ['episode_number', 'audio_en', 'audio_fr', 'audio_status', 'subs_en', 'subs_fr', 'subs_status', 'name'])
            data += '<br/><br/>'

        return render_template('series.html', TV_SHOW=serie_name, EPISODE_LIST=[data])


    @app.route('/<serie_name>-Debug')
    def serie_debug_view(serie_name):
        episodes = db_collection.find({ "tv_show" : serie_name })

        df = pandas.DataFrame(data=episodes)
        df = df.fillna(' ').T

        data = df.to_html(classes='data', header="true")

        return render_template('series.html', TV_SHOW=serie_name, EPISODE_LIST=[data])

    app.run(debug=True)

if __name__ == '__main__':
    main()
