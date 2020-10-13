from flask import jsonify, redirect, request
from datetime import datetime
from src import app, scheduler
from .spotify_auth import SpotifyAuth
from .spotify_fetcher import SpotifyFetcher

@app.route("/")
def helloWorld():
    if not scheduler.get_job('fetch'):
        return redirect("http://localhost:5000/auth/authorize")
    releases = []
    return jsonify(releases)

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
    
    access_token = response.get('access_token')
    expires_in = response.get('expires_in')
    refresh_token = response.get('refresh_token')
    spotifyFetcher = SpotifyFetcher(access_token, expires_in, refresh_token)
    scheduler.add_job(func=spotifyFetcher.import_releases, id="fetch", replace_existing=True, trigger='interval', hours=12, next_run_time=datetime.now())
    return redirect("http://localhost:5000")

