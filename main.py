import os
import sys
from flask import Flask, render_template, send_from_directory
import logging

import model_firebase as model
import config

app = Flask(__name__)
app.config.from_object(config)

model.init_app(app)

@app.route("/")
def index():
    a = model.Achievement.GetAll()
    a.reverse()
    players = model.Player.GetAll()
    posts = model.Post.GetAll()
    print(posts)
    online_players = [x for x in players if x.is_online]
    offline_players = [x for x in players if not x.is_online]
    offline_players.reverse()
    return render_template('index.html', online_players=online_players,
                           offline_players=offline_players, achievements=a,
                           posts=posts)

@app.route("/initial")
def initial():
    return render_template('first_time.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')
if __name__ == "__main__":
    app.run()
