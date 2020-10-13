# ChallengeBackend

Your goal is to create an app using the [spotify web api](https://developer.spotify.com/documentation/web-api/). You can make for example a [Flask](https://flask.palletsprojects.com/en/1.1.x/) or [Django rest framework](https://www.django-rest-framework.org/) project, it has to be able to authenticate to Spotify to fetch the new releases. Your job is to add two new features:
- A way to fetch data from spotify’s new releases API (/v1/browse/new-releases) and persist in a Postgresql DB (mandatory)
- A route : `/api/artists/` returning a JSON containing informations about artists that have released new tracks recently, from your local copy of today’s spotify’s new releases.

## Project Structure
The spotify auth is provided by us: (follows spotify web api.): it is located in `spotify_auth.py`.
The flow ends with a call to `/auth/callback/` which will give you the necessary access tokens.
To use it, we will provide you with the necessary: CLIENT_ID and CLIENT_SECRET.
Feel free to move it and re-organise as you please, we expect a well organised and clean code.
  
  
## Tech Specifications
- Be smart in your token usage (no unnecessary refreshes)
- Don’t request spotify artists at each request we send you
- The way you store the artists in Postgresql DB is going to be important use an ORM.
- As stated above, to test your server we will `GET /api/artists/` and we expect a nicely organised payload of artists. Make sure to use proper serialization and handle http errors.

All stability, performance, efficiency adds-up are highly recommended.

## Installation
First you'll need to clone the repo
```
$ git clone https://github.com/ecralx/ChallengeBackend.git && cd ChallengeBackend
$ cp .env.example .env
```

Modify the `.env` file according to your needs (you'll need to specify the spotify client_id/client_secret, and eventually you database url if you don't use Docker).

If you have Docker run the following:
```
$ git clone https://github.com/ecralx/ChallengeBackend.git && cd ChallengeBackend
$ docker-compose build
$ docker-compose run
```

And if you don't:
```
$ python -m venv ./env
$ source ./env/bin/activate
$ pip install requirements.txt
$ python manage.py create_db
$ python manage.py run -h 0.0.0.0
```

Once you're done, visit [http://localhost:5000/api/artists](http://localhost:5000/api/artists) !

## Various remarks
This part is kind-of a todo list to what could be done. I did want to make the app in ~one day.

- The token is being refreshed only when Spotify's API specifies that it is expired. Sadly the best way to do that is to compare the error message (no specific status code is used).
- I've made some modifications in the refreshAuth as it didn't correspond to the (Spotify) documentation's specifications.
- I didn't want to alter `SpotifyAuth` any further, so I didn't change the hardcoded callback url for something more automated.
- I'm using the spotify-ids as primary keys as the app is only centered on Spotify. Obviously, it doesn't scale well (if later we want to add data from other sources) but I thought it met the needs (and it was cool to test for once another primary key setup).
- I'm scheduling the call to Spotify's `new-releases` endpoint every 15 seconds, which is clearly an overkill but I made it that way to test that duplicates are well handled.
- I'm logging errors (specially for the requests made to Spotify's API) and some information about the data fetched/inserted (hence `docker-compose run` and not `docker-compose run -d`).
- To make it as simple as possible, the `api/artists` will display a JSON containing the artists that made the latest 20 albums. You can change the value by changing in the url the `release_limit`: [http://localhost:5000/api/artists?release_limit=10](http://localhost:5000/api/artists?release_limit=10).