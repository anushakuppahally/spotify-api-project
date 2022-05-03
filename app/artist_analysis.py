import os
import spotipy
import requests
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

def GetArtist(artist):
    result = spotify.search(artist) #search query
    artist_uri = result['tracks']['items'][0]['artists'][0]['uri']
    return artist_uri

def ArtistAlbums(artist_uri): #returns the artist's albums
    artistalbums = []
    r = requests.get(BASE_URL + 'artists/' + str(artist_uri[15:]) + '/albums', 
                 headers=headers,
                 params={'include_groups': 'album', 'limit': 50})
    d = r.json()
    for album in d['items']: #returns the artist's albums and their release date and the number of total tracks 
        artistalbums.append((album['name'], 'Released:', album['release_date'],'Total Tracks:', album['total_tracks']))
    return artistalbums

def ArtistTopTracks(artist_uri): #returns artist's top 5 tracks
    artisttracks = []
    tracks = spotify.artist_top_tracks(artist_uri,country='US')
    for top in tracks['tracks'][:5]: #returns top 5 tracks in the US 
        artisttracks.append(top['name'])
    return artisttracks

def ArtistSongRecommendations(artist_uri): #returns 5 song recommendations based on the artist
    songrecs = []
    recs = spotify.recommendations(seed_artists=[artist_uri],limit = 5)
    for track in recs['tracks']: #returns recommended tracks 
        songrecs.append((track['name'],"by",track['artists'][0]['name'])) #returns track name and artist
    return songrecs

def ArtistRecs(artist_uri): #returns 5 artist recommendations based on the artist 
    artistrecs = []
    relatedartists = spotify.artist_related_artists(artist_uri)
    for person in relatedartists['artists'][:5]: #returns related artists 
        artistrecs.append(person['name'])
    return artistrecs