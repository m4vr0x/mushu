import logging
import pymongo
import pandas
from flask import Flask,render_template,request,json

import scripts

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d_%H:%M:%S', level=logging.DEBUG)

app = Flask(__name__)

db_client, database, collection = scripts.setup_db_client()

@app.route("/")
def homepage():
    mesg = ("Starting homepage")
    logging.info(mesg)
    return render_template('home.html.jinja')

@app.route('/test_db')
def test_db():
    msg = scripts.test_db_connection(db_client)
    return render_template('home.html.jinja', result=msg)

@app.route('/scan_dir')
def scan_dir():
    dir_path = "/files"
    series_list = scripts.populate_db(dir_path, db_client, collection)
    return render_template('scan-page.html.jinja', series_list=series_list)

@app.route('/<show_name>')
def serie_view(show_name):
    episodes = collection.find({ "tv_show" : show_name })
    df = pandas.DataFrame(data = episodes)
    logging.debug("df")
    logging.debug(df)

    for path in df['full_path']:
        logging.info(path)
        scripts.media_info(collection, path)

    data = df.to_html(index=False, justify="left", columns = ['season_number', 'episode_number', 'name', 'resolution', 'audio_en', 'subs_en', 'audio_fr', 'subs_fr'])

    # df_full = pandas.DataFrame(data = episodes)
    # logging.debug(df_full)
    # logging.debug("df_full")
    #
    # season_list = df_full.season_number.unique()
    # for season in season_list:
    #     season_table = df_full[df_full['season_number'] == season]
    #     data += season_table.to_html(index=False, justify="left", columns = ['episode_number', 'audio_en', 'audio_fr', 'audio_status', 'subs_en', 'subs_fr', 'subs_status', 'name'])

    return render_template('show-page.html.jinja', log='', show=show_name, episode_list=[data])

if __name__ == '__main__':
    app.run(host='0.0.0.0')
