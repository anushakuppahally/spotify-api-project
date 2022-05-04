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
    '''
    This function returns the URI of an artist 
    Once a user inputs an artist, the function can be invoked as GetArtist(artist)
    Example return value: "spotify:artist:06HL4z0CvFAxyc27GXpf02"
    The URI can then be used in other functions to return information about the artist, recommendations, and more
    '''
    result = spotify.search(artist) #search query
    artist_uri = result['tracks']['items'][0]['artists'][0]['uri']
    return artist_uri

def ArtistAlbums(artist_uri):
    '''
    This function returns all of an artist's albums, with their release date and number of total tracks 
    Once the artist's URI is returned, this function uses that as an input
    Then, the function will return tuples with the information 
    Example return value: ('1989', 'Released:', '2014-10-27', 'Total Tracks:', 13)
    '''
    artistalbums = []
    r = requests.get(BASE_URL + 'artists/' + str(artist_uri[15:]) + '/albums', 
                 headers=headers,
                 params={'include_groups': 'album', 'limit': 50})
    d = r.json()
    for album in d['items']: #returns the artist's albums and their release date and the number of total tracks 
        artistalbums.append((album['name'], 'Released:', album['release_date'],'Total Tracks:', album['total_tracks']))
    return artistalbums

def ArtistTopTracks(artist_uri): #returns artist's top 5 tracks
    '''
    This function returns the artist's top 5 tracks 
    This function uses the artist's URI as an input 
    Then, the function returns a list of strings with this information 
    Example return value: ["All Too Well (10 Minute Version) (Taylor's Version) (From The Vault)", 'Blank Space', 'Lover', "Wildest Dreams (Taylor's Version)", 'The Joker And The Queen (feat. Taylor Swift)']
    '''
    artisttracks = []
    tracks = spotify.artist_top_tracks(artist_uri,country='US')
    for top in tracks['tracks'][:5]: #returns top 5 tracks in the US 
        artisttracks.append(top['name'])
    return artisttracks

def ArtistSongRecommendations(artist_uri): #returns 5 song recommendations based on the artist
    '''
    This function returns 5 song recommendations 
    This function uses the artist's URI as an input 
    Then, the function returns a list of tuples
    An example tuple: ('Adore You', 'by', 'Harry Styles')
    '''
    songrecs = []
    recs = spotify.recommendations(seed_artists=[artist_uri],limit = 5)
    for track in recs['tracks']: #returns recommended tracks 
        songrecs.append((track['name'],"by",track['artists'][0]['name'])) #returns track name and artist
    return songrecs

def ArtistRecs(artist_uri): #returns 5 artist recommendations based on the artist 
    '''
    This function returns 5 artist recommendations
    This function uses the artist's URI as an input
    Then, the function returns a list of strings 
    Example string: 'Demi Lovato'
    '''
    artistrecs = []
    relatedartists = spotify.artist_related_artists(artist_uri)
    for person in relatedartists['artists'][:5]: #returns related artists 
        artistrecs.append(person['name'])
    return artistrecs