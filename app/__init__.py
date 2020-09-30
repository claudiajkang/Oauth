from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='template')
app.config.from_object('config')

db = SQLAlchemy(app)

from app.model import *

db.create_all()

from app.oauth2 import config_oauth

config_oauth(app)
