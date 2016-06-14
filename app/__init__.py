import os
basedir = os.path.abspath(os.path.dirname(__file__))
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__, static_folder='../static')
Bootstrap(app)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models