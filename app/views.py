from flask import render_template
from app import app

@app.route('/')
def home():
   return render_template('home.html')

# @app.route('/')
# def home():
#     return render_template('home.html', SHOW_LIST=show_list, B=db_name)

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
