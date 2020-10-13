import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler

app = Flask(__name__)
app.config.from_object("src.config.Config")
db = SQLAlchemy(app)
scheduler = APScheduler()
scheduler.start()

from .models import *
from .routes import *