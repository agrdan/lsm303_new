from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from configs.config import DevConfig

NAME = "self"
app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)
