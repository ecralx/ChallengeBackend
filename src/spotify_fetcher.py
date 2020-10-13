from .spotify_auth import SpotifyAuth
from datetime import datetime
from math import ceil
import requests, json

class SpotifyFetcher(SpotifyAuth):
    SPOTIFY_URL_NEW_RELEASES = "https://api.spotify.com/v1/browse/new-releases"
    SPOTIFY_LIMIT_NEW_RELEASES = 50
    SPOTIFY_EXPIRATION_MESSAGE = "The access token expired"

    def __init__(self, access_token, expires_in, refresh_token):
        self.__set_init(access_token, expires_in, refresh_token)

    def __set_init(self, access_token, expires_in, refresh_token):
        self.__access_token = access_token
        self.__expires_in = expires_in
        self.__refresh_token = refresh_token
        self.__access_token_time = datetime.now().timestamp()

    def request(self, offset=0):
        headers = {
            "Authorization": f"Bearer {self.__access_token}"
        }
        url = f"{self.SPOTIFY_URL_NEW_RELEASES}?limit={self.SPOTIFY_LIMIT_NEW_RELEASES}&offset={offset}"
        response = requests.get(url, headers=headers)
        response_data = json.loads(response.text)
        #TODO add waiting if spotify tells us so
        if response_data.get('error'):
            if response_data.get('error').get('status') == 401 and response_data.get('error').get('message') == self.SPOTIFY_EXPIRATION_MESSAGE:
                # refresh token only when we're told to
                auth_resp = self.refreshAuth(self.__refresh_token)
                access_token = auth_resp.get('access_token')
                expires_in = auth_resp.get('expires_in')
                refresh_token = auth_resp.get('refresh_token')
                self.__set_init(access_token, expires_in, refresh_token)
                return self.request(offset)
        return response_data
    
    def fetch_all(self):
        releases = []
        offset = 0
        first_batch = self.request()
        if "error" in first_batch:
            #TODO log something and stop it here
            return []
        releases += first_batch.get('albums').get('items')
        total = first_batch.get('albums').get('total')
        nb_pages = ceil(total / self.SPOTIFY_LIMIT_NEW_RELEASES)
        if nb_pages > 1:
            for i in range(1, nb_pages):
                offset = i * self.SPOTIFY_LIMIT_NEW_RELEASES
                batch = self.request(offset)
                if "error" in batch:
                    #TODO log something and stop it here
                    return []
                releases += batch.get('albums').get('items')

        return releases