from inspect import getargs
import os
import spotipy
import logging
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

logger = logging.getLogger('examples.artist_recommendations')
logging.basicConfig(level='INFO')

def GetArtist(artist):
    result = spotify.search(artist) #search query
    artist_uri = result['tracks']['items'][0]['artists'][0]['uri']
    return artist_uri

def ArtistMusic(artist_uri):
    r = requests.get(BASE_URL + 'artists/' + str(artist_uri[15:]) + '/albums', 
                 headers=headers,
                 params={'include_groups': 'album', 'limit': 50})
    d = r.json()
    print("Here are the artist's albums:")
    for album in d['items']:
        print(album['name'], ' — Released:', album['release_date'],' — Total Tracks:', album['total_tracks'])
    print("") #spacing
    print("Here are the artist's top tracks in the US:")
    tracks = spotify.artist_top_tracks(artist_uri,country='US')
    for top in tracks['tracks'][:5]: #returns top 5 tracks in the US 
        print(top['name'])
    print("")

def ArtistRecommendations(artist_uri):
    recs = spotify.recommendations(seed_artists=[artist_uri])
    print("Here are recommended tracks based on the artist entered:")
    for track in recs['tracks']:
        print(track['name'],"by",track['artists'][0]['name']) #returns track name and artist
    print("") #spacing
    print("Here are some other related artists based on the artist entered:")
    artistrecs = spotify.artist_related_artists(artist_uri)
    for person in artistrecs['artists']:
        print(person['name'])

def main():
    artist = input("Please enter the name of an artist: ")
    try:
        artist_uri = GetArtist(artist)
        print("") #spacing
        ArtistMusic(artist_uri)
        print("") #spacing
        ArtistRecommendations(artist_uri)
        print("") #spacing
        
    except:
        print("Can't find that artist, try again.")
        return None

if __name__ == '__main__':
    main()