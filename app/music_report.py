import os
import spotipy
import time
import pandas as pd
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

import artist_uri from app.artist_analysis

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL_ADDRESS = os.getenv("SENDER_EMAIL_ADDRESS")
CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

def AudioAnalysis():
    #create a dataframe with all of the tracks from the artist selected by the user 
    #then create averages/graphs with this information  