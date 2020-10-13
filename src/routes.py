from flask import jsonify, redirect, request, url_for
from datetime import datetime, date
from src import app, db, scheduler, Album, Artist
from .spotify_auth import SpotifyAuth
from .spotify_fetcher import SpotifyFetcher

@app.route("/api/artists")
def todayArtists():
    """
    Displays the artists of the last <release_limit, default:20> releases.
    """
    limit = request.args.get('release_limit', 20)

    if not scheduler.get_job('fetch'):
        return redirect(url_for('authLogin'))
    latest_releases = Album.query.order_by(Album.created_at.desc()).limit(limit).all()
    if len(latest_releases) > 0:
        artist_idx = []
        artists = []
        for release in latest_releases:
            for artist in release.artists:
                if not artist.id in artist_idx: # uniques only
                    artists.append(artist)
                    artist_idx.append(artist.id)
    else:
        artists = []
    return jsonify({
        "items": [artist.serialize() for artist in artists],
        "count": len(artists)
    })

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
    scheduler.add_job(
        func=spotifyFetcher.import_releases,
        id="fetch",
        replace_existing=True,
        trigger='interval',
        seconds=15,
        next_run_time=datetime.now()
    )
    return redirect(url_for('todayArtists'))

