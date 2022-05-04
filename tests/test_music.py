from app.music_report import GetCharacteristics

import os
import pytest
import spotipy
import requests
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

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

#convert the response to json
auth_response_data = auth_response.json()

#save the access token
access_token = auth_response_data['access_token']
headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}

id = "spotify:track:51QEyJI5M7uyd8DOh9tqQY" #Buzzcut Season by Lorde

@pytest.mark.skipif(os.getenv("CI")=="true", reason="avoid issuing on the CI server") # skips this test on CI
def test_getcharacteristics():
    results = GetCharacteristics(id)
    assert len(results) == 15
    assert isinstance(results, list)
    assert isinstance(results[4],int) #length
    assert isinstance(results[14],int) #time signature
    assert isinstance(results[6],float) #acousticness
    assert isinstance(results[1],str) #album

def test_dummy():
    assert 2 + 2 == 4