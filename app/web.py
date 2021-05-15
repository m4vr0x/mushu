import logging
import time
import pymongo
import pandas
from flask import Flask, render_template, request, redirect, url_for, json
import json

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

@app.route('/series_list')
def show_scan_page():
    return render_template('series_list.html.jinja', series_list=series_list)

@app.route('/series_scan')
def show_scan_page():
    series_list = scripts.populate_db(dir_path, db_client, collection)
    return render_template('series_scan.html.jinja', series_list=series_list)

@app.route('/shows')
def show_list_view():
    # dir_path = "/files"
    # series_list = scripts.populate_db(dir_path, db_client, collection)
    return render_template('scan-page.html.jinja', series_list=series_list)
 
# def serie_view(show_name):
    # episodes = collection.find({ "tv_show" : show_name })
    # df = pandas.DataFrame(data = episodes)
    # logging.debug("df")
    # logging.debug(df)
    #
    # for path in df['full_path']:
    #     logging.info(path)
    #     scripts.media_info(collection, path)
    #
    # data = df.to_html(index=False, justify="left", columns = ['season_number', 'episode_number', 'name', 'resolution', 'audio_en', 'subs_en', 'audio_fr', 'subs_fr'])

    # df_full = pandas.DataFrame(data = episodes)
    # logging.debug(df_full)
    # logging.debug("df_full")
    #
    # season_list = df_full.season_number.unique()
    # for season in season_list:
    #     season_table = df_full[df_full['season_number'] == season]
    #     data += season_table.to_html(index=False, justify="left", columns = ['episode_number', 'audio_en', 'audio_fr', 'audio_status', 'subs_en', 'subs_fr', 'subs_status', 'name'])

    # return render_template('show-page.html.jinja', log='', show=show_name, episode_list=[data])

@app.route('/wip')
def working():
    return render_template('working.html.jinja')

@app.route('/full_scan')
def full_scan():
    dir_path = "/files"
    series_list = scripts.populate_db(dir_path, db_client, collection)

    redirect(url_for('working'))

    for show in collection.distinct("tv_show"):
        episodes = collection.find({ "tv_show" : show })
        df = pandas.DataFrame(data = episodes)
        for path in df['full_path']:
            logging.info(path)
            scripts.media_info(collection, path)

    # data = df.to_html(index=False, justify="left", columns = ['season_number', 'episode_number', 'name', 'resolution', 'audio_en', 'subs_en', 'audio_fr', 'subs_fr'])

    return redirect(url_for("show_list_view"))


### TEST AJAX ###
@app.route('/signUp')
def signUp():
    return render_template('signUp.html')

@app.route('/signUpUser', methods=['POST'])
def signUpUser():
    user =  request.form['username'];
    password = request.form['password'];
    return json.dumps({'status':'OK','user':user,'pass':password});

### TEST ###
"""Focusing on just this route that display a linechart for the sentiment of a topic over time."""
@app.route('/line', methods =["GET"])
def line_chart():
  """
  Doing a bunch of python
  Using a small example data set.
  """
  data = json.dumps( [1.0,2.0,3.0] )
  labels=json.dumps( ["12-31-18", "01-01-19", "01-02-19"] )
  return render_template("linechart.html", data = data,
                        labels=labels)
### TEST ###

if __name__ == '__main__':
    app.run(host='0.0.0.0')
