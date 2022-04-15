from inspect import getargs
import os
#from app.music_report import CLIENT_CREDENTIALS_MANAGER
import spotipy
import sys
import time
import requests
import pandas as pd
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
BASE_URL = 'https://api.spotify.com/v1/'
AUTH_URL = 'https://accounts.spotify.com/api/token'
auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })

# convert the response to JSON
auth_response_data = auth_response.json()

# save the access token
access_token = auth_response_data['access_token']
headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}

#def GetArtist():
    #artist = input("Please enter the name of an artist: ")
    #artist_id = id(artist)
    #artist='Birdy'
    #artist_id='spotify:artist:2WX2uTcsvV5OnS0inACecP'

def ArtistAlbums(artist_id):
    r = requests.get(BASE_URL + 'artists/' + str(artist_id) + '/albums', 
                 headers=headers,
                 params={'include_groups': 'album', 'limit': 50})
    d = r.json()
    for album in d['items']:
        print(album['name'], ' --- Released:', album['release_date'],' --- Total Tracks:', album['total_tracks'])


def main():
    artist_id='2WX2uTcsvV5OnS0inACecP'
    #artist_id=GetArtist()
    #if artist_id:
    ArtistAlbums(artist_id)
    #else:
    #    print("Can't find that artist, try again.")

if __name__ == '__main__':
    main()

#artist='Birdy'
#artist_id='spotify:artist:2WX2uTcsvV5OnS0inACecP'