import os
import spotipy
import pandas as pd
import requests
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from spotipy.oauth2 import SpotifyClientCredentials
import plotly.express as px

from app.artist_analysis import GetArtist

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL_ADDRESS = os.getenv("SENDER_EMAIL_ADDRESS")
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


def AudioAnalysis(artist_uri):
    #creates a dataframe with all of the tracks from the artist selected by the user 
    #then creates data visualizations with this information  
    
    r = requests.get(BASE_URL + 'artists/' + str(artist_uri[15:]) + '/albums', 
                    headers=headers,
                    params={'include_groups': 'album', 'limit': 50})
    d = r.json()
    
    albums = [] #holds album ids for an artist 
    
    for album in d['items']:
        album_ids = album['id']
        albums.append(str(album_ids))

    ids = []

    for album in albums:
        tracks = spotify.album_tracks(album)
        for item in tracks:
            track = item['track']
            ids.append(track['id'])
        return ids


    #data features
    #df = pd.DataFrame(tracks, columns = ['name','album','artist','release_date','length','popularity','danceability','acousticness','energy','instrumentalness','liveness','loudness','speechiness','tempo','time_signature'])

def main():
    artist = input("Please enter the name of an artist that you want an email report: ")
    try:
        artist_uri = GetArtist(artist)
        AudioAnalysis(artist_uri)
    except:
        print("Can't find that artist, try again.")
        return None

if __name__ == '__main__':
    main()