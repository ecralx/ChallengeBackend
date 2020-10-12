from flask import jsonify, redirect, request
from src import app
from .spotify_auth import SpotifyAuth

@app.route("/")
def helloWorld():
    return jsonify(hello="world")

@app.route("/auth/authorize")
def authLogin():
    spotify = SpotifyAuth()
    redirect_link = spotify.getUser()
    return redirect(redirect_link)

@app.route("/auth/callback")
def authCallback():
    error = request.args.get('error')
    if error:
        return jsonify({
            'status': 'error',
            'error': error
        }), 500
    code = request.args.get('code')

    spotify = SpotifyAuth()
    response = spotify.getUserToken(code)
    if "error" in response:
        return jsonify({
            'status': 'error',
            'error': response
        }), 500
    
    # Make the magic here :)
    return jsonify(response)

