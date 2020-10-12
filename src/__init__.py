import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("src.config.Config")
db = SQLAlchemy(app)

from .models import *
from .routes import *