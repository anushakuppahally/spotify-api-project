import os
#from app.music_report import CLIENT_CREDENTIALS_MANAGER
import spotipy
import sys
import time
import pandas as pd
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

#def ArtistInfo():
artist = input("Enter the name of an artist: ") #add data validation
artist_id = id(artist)
results = spotify.artist_albums(artist_id, album_type='album')
albums = results['items']
while results['next']:
    results = spotify.next(results)
    albums.extend(results['items'])

print("Here are all of the artist's albums:")
for album in albums:
    print(album['name'])

print("Here are", artist + "'s top 10 tracks in the US:")
top10tracks = artist_top_tracks(artist_id,country='US')
for track in top10tracks:
    print(track['name'])


#def SongInfo():
    #returns analysis of a song

#def Recommendations():
    #returns recommendations based on artist and song entered previously