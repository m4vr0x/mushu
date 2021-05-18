import logging
import pymongo
import pandas
from flask import Flask,render_template,request,json
from tabulate import tabulate

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
    try:
        series_list = scripts.populate_db(dir_path, db_client, collection)
        return render_template('scan-page.html.jinja', series_list=series_list)
    except Exception as exception:
        return render_template('error-page.html.jinja', exception=exception)

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
    except Exception :
        raise

@app.route('/<show_name>')
def serie_view(show_name):
    paths_list = collection.find({ "tv_show" : show_name },{ "_id": 0, "full_path": 1 })

    for r in paths_list:
        path = r['full_path']
        logging.info(path)
        #Analyse media file using path and append to db
        try:
            scripts.media_info(collection, path)
        except Exception as exception:
            return render_template('error-page.html.jinja', exception=exception)
            
    episodes = collection.find({ "tv_show" : show_name })
    episodes_df = pandas.DataFrame(data = episodes)
    ### DEBUG ###
    # msg = (tabulate(episodes_df, headers='keys', tablefmt='psql'))
    # logging.debug(f'episodes_df:\n {msg}')
    ### DEBUG ###

    data_html = episodes_df.to_html(index=False, justify="left", columns = ['season_number', 'episode_number', 'name', 'resolution', 'audio_en', 'subs_en', 'audio_fr', 'subs_fr'])
    ### DEBUG ###
    # logging.debug(f'data: {data_html}')
    ### DEBUG ###

    return render_template('show-page.html.jinja', log='', show=show_name, episode_list=[data_html])

if __name__ == '__main__':
    app.run(host='0.0.0.0')
