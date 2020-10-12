from flask import jsonify
from src import app

@app.route("/")
def hello_world():
    return jsonify(hello="world")