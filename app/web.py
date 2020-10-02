import logging
import pymongo
from flask import Flask,render_template,request

import scripts

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d_%H:%M:%S', level=logging.DEBUG)

app = Flask(__name__)

@app.route("/")
def homepage():
    mesg = ("Starting homepage")
    logging.info(mesg)
    return render_template('home.html')

@app.route('/test_db')
def test_db():
    status = scripts.test_db_connection()
    return render_template('home.html', result=status)

@app.route('/scan_dir')
def scan_dir():
    # status = scripts.test_db_connection()
    return render_template('scan.html')

# @app.route('/analyse_media_directory')
# def scan_dir():
#     status = scripts.test_db_connection()
#     return render_template('home.html', result=status)

# @app.route('/<serie_name>')
# def serie_view(serie_name):
#     episodes = db_collection.find({ "tv_show" : serie_name })
#
#     df = pandas.DataFrame(data = episodes)
#     season_list = df.season_number.unique()
#
#     data = ''
#
#     for season in season_list:
#         season_table = df[df['season_number'] == season]
#
#         data += 'Season '+season+'<br/><br/>'
#         data += season_table.to_html(index=False, justify="left", columns = ['episode_number', 'audio_en', 'audio_fr', 'audio_status', 'subs_en', 'subs_fr', 'subs_status', 'name'])
#         data += '<br/><br/>'
#
#     return render_template('series.html', TV_SHOW=serie_name, EPISODE_LIST=[data])
#
#
# @app.route('/<serie_name>-Debug')
# def serie_debug_view(serie_name):
#     episodes = db_collection.find({ "tv_show" : serie_name })
#
#     df = pandas.DataFrame(data=episodes)
#     df = df.fillna(' ').T
#
#     data = df.to_html(classes='data', header="true")
#
#     return render_template('series.html', TV_SHOW=serie_name, EPISODE_LIST=[data])
#
#     app.run(debug=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
