from flask import Flask, render_template, request
import requests
from data.hero_data import hero_names  # Импортируем словарь с именами героев

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    match_data = None
    match_id = None

    if request.method == 'POST':
        match_id = request.form['match_id']
        match_data = get_match_data(match_id)

    return render_template('index.html', match_data=match_data, match_id=match_id)


def get_match_data(match_id):
    url = f'https://api.opendota.com/api/matches/{match_id}'
    response = requests.get(url)
    if response.status_code == 200:
        match_data = response.json()
        for player in match_data['players']:
            hero_id = player.get('hero_id')
            player['hero_name'] = hero_names.get(hero_id, 'Unknown Hero')  # Подставляем имя героя
        return match_data
    else:
        return None


if __name__ == '__main__':
    app.run(debug=True)
