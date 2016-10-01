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
    p = None
    return render_template('index.html', posts=p, achievements=a)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')
if __name__ == "__main__":
    app.run()
