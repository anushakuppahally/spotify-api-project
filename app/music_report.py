from inspect import getargs
import os
import sys
import spotipy
import pandas as pd
import seaborn as sns
import requests
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition, ContentId
import base64
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt

#using function output in email
from app.artist_analysis import GetArtist
from app.artist_analysis import ArtistAlbums
from app.artist_analysis import ArtistTopTracks
from app.artist_analysis import ArtistSongRecommendations
from app.artist_analysis import ArtistRecs

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL_ADDRESS = os.getenv("SENDER_ADDRESS")
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


#analyzes the tracks of the entered artist and returns insights in an email report, along with artist analysis and recommendations
def AudioAnalysis(artist_uri):
    '''
    This function takes artist URI as an input
    Then, the function creates a dataframe with all of the tracks from the artist URI by calling the GetCharacteristics function
    After this, the function tests the correlation between popularity and the characteristics
    The function identifies the variables most and least correlated
    Then, the function creates visualizations: a histogram of popularity and scatterplots of popularity vs the most and least correlated variables
    After that, the function creates the email report with the information from artist_analysis
    The function also attachs the visualizations and a CSV file
    The function output will be '202' if the email is sent successfully  
    '''
    
    r = requests.get(BASE_URL + 'artists/' + str(artist_uri[15:]) + '/albums', 
                    headers=headers,
                    params={'include_groups': 'album', 'limit': 50})
    d = r.json()
    
    albums = [] #holds album ids for an artist 
    
    for album in d['items']:
        album_ids = album['id']
        albums.append(str(album_ids))

    ids = [] #holds track ids 

    for album in albums:
        songs = spotify.album_tracks(album)
        for item in songs['items']: #getting track ids for each track in each album
            track = item['id']
            ids.append(track)

    #data features

    tracks = []

    for i in range(len(ids)):
        id = ids[i]
        track = GetCharacteristics(id)
        tracks.append(track)

    #creates dataframe with each track's characteristics
    df = pd.DataFrame(tracks, columns = ['name','album','artist','release_date','length','popularity','acousticness','danceability','energy','instrumentalness','liveness','loudness','speechiness','tempo','time_signature'])

    #getting features
    popularity = df["popularity"]
    
    #factors to calculate correlation with population
    df2 = df[['acousticness','danceability','energy','instrumentalness','liveness','loudness','speechiness','tempo','time_signature']].copy()

    correlations = [] #storing the correlations between each variable and popularity 

    #calculating the correlation between each feature and population 
    for j in df2:
        var = df[str(j)]
        corr = popularity.corr(var)
        correlations.append(corr)

    #finding the variable most correlated with popularity 
    max_corr = max(correlations) 
    max_corr_index = correlations.index(max_corr)

    #finding the variable least correlated with popularity 
    min_corr = min(correlations) 
    min_corr_index = correlations.index(min_corr)

    #data visualizations
    script_dir = os.path.dirname(__file__)
    reports_dir = os.path.join(script_dir,"..", 'reports/ ')
    
    #popularity histogram 
    popularity.plot(kind='hist', color='purple',edgecolor='black',title='Popularity Histogram')
    pop_file_name = "pophist.png"
    plt.savefig(reports_dir + pop_file_name)

    #scatterplot of variable most correlated with popularity 
    sns.lmplot(x = str(df2.columns[max_corr_index]),y = 'popularity',data=df,fit_reg = True)
    scat_file_name1 = "most_correlated.png"
    plt.savefig(reports_dir + scat_file_name1)

    #scatterplot of variable least correlated with popularity 
    sns.lmplot(x = str(df2.columns[min_corr_index]),y = 'popularity',data=df,fit_reg = True)
    scat_file_name2 = "least_correlated.png"
    plt.savefig(reports_dir + scat_file_name2)

    artist_albums = ArtistAlbums(artist_uri)
    artist_top = ArtistTopTracks(artist_uri)
    artist_songrecs = ArtistSongRecommendations(artist_uri)
    artist_recs = ArtistRecs(artist_uri)
    artist = spotify.artist(artist_uri)['name']

    #email
    subject="[Email Report]: Artist Analysis"
    
    html=f"<h2>Analysis of {artist}'s Discography</h3>"

    html+=f"<h3>Information about {artist}</h3>"
    
    html+=f"<h4>Here are {artist}'s album(s):</h4>"

    #looping through first function to get artist albums
    for i in artist_albums:
        html+=f"<p>{i[0]+', '+i[1]+' '+i[2]+', '+i[3]+' '+str(i[4])}</p>"
    
    html+=f"<h4>Here are {artist}'s top 5 tracks:</h4>"

    #looping through second function to get the artist's top 5 tracks 
    for j in artist_top:
        html+=f"<p>{j}</p>"
    
    html+=f"<h4>Here are 5 song recommendations based on {artist}:</h4>"
    for x in artist_songrecs:
        html+=f"<p>{x[0] + ' ' + x[1] + ' ' + x[2]}</p>"
    
    html+=f"<h4>Here are 5 artist recommendations based on {artist}:</h4>"
    for g in artist_recs:
        html+=f"<p>{g}</p>"

    html+="<h3>Song Characteristics Analysis:</h3>"

    html+=f"<h4>Data visualization based on {artist}'s discography:</h4>"
    
    html+="<p>See attached images for a histogram of popularity, a scatterplot between popularity and the most correlated variable, and a scatterplot between popularity and the least correlated variable.</p>"
    
    html+=f"<h4>See the attached CSV file for the characteristics of each song by {artist}</h4>"

    html+="<p>Thank you!</p>"

    client = SendGridAPIClient(SENDGRID_API_KEY) 
    message = Mail(from_email=SENDER_EMAIL_ADDRESS, to_emails=SENDER_EMAIL_ADDRESS, subject=subject, html_content=html)
    
    #creating csv
    encoded_csv = base64.b64encode(df.to_csv(index=False).encode()).decode()
    
    #attaching csv
    message.attachment = Attachment(
    file_content = FileContent(encoded_csv),
    file_type = FileType('text/csv'), 
    file_name = FileName('spotify_report.csv'), 
    disposition = Disposition('attachment'),
    content_id = ContentId('Attachment 1')
    )

    #attaching images
    
    #attaching popularity histogram 
    with open(reports_dir + pop_file_name, 'rb') as f:
        data = f.read()
        f.close()
    encoded_img1 = base64.b64encode(data).decode()
    
    message.attachment = Attachment(
    file_content = FileContent(encoded_img1),
    file_type = FileType('image/png'), 
    file_name = FileName('pophist.png'), 
    disposition = Disposition('inline'),
    content_id = ContentId('Attachment 2')
    )

    #attaching scatterplot of most correlated variable 
    with open(reports_dir + scat_file_name1, 'rb') as g:
        data = g.read()
        g.close()
    encoded_img2 = base64.b64encode(data).decode()
    
    message.attachment = Attachment(
    file_content = FileContent(encoded_img2),
    file_type = FileType('image/png'), 
    file_name = FileName('most_correlated.png'), 
    disposition = Disposition('inline'),
    content_id = ContentId('Attachment 3')
    )

    #attaching scatterplot of least correlated variable 
    with open(reports_dir + scat_file_name2, 'rb') as h:
        data = h.read()
        h.close()
    encoded_img3 = base64.b64encode(data).decode()
    
    message.attachment = Attachment(
    file_content = FileContent(encoded_img3),
    file_type = FileType('image/png'), 
    file_name = FileName('least_correlated.png'), 
    disposition = Disposition('inline'),
    content_id = ContentId('Attachment 4')
    )

    #send email 
    response = client.send(message)
    print(response.status_code) #202 means success

#returns characteristics for a track id
def GetCharacteristics(id):
    '''
    This function returns the characteristics for a track
    This function uses a track's ID as an input 
    Then, this function returns a list of strings, floats, and integers
    Example output: ['Buzzcut Season', 'Pure Heroine', 'Lorde', '2013-09-27', 246755, 67, 0.606, 0.733, 0.62, 0.305, 0.117, -10.525, 0.075, 111.039, 4]
    '''
    meta = spotify.track(id)
    features = spotify.audio_features(id)
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    release_date = meta['album']['release_date']
    length = meta['duration_ms']
    popularity = meta['popularity']

    #song features
    acousticness = features[0]['acousticness']
    danceability = features[0]['danceability']
    energy = features[0]['energy']
    instrumentalness = features[0]['instrumentalness']
    liveness = features[0]['liveness']
    loudness = features[0]['loudness']
    speechiness = features[0]['speechiness']
    tempo = features[0]['tempo']
    time_signature = features[0]['time_signature']

    track = [name, album, artist, release_date, length, popularity, acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, tempo, time_signature]
    return track

def main():
    artist = input("Please enter the name of an artist that you want an email report: ") #user input
    try:
        artist_uri = GetArtist(artist)
    except:
        print("Can't find that artist, try again.") #error handling
        sys.exit()
    else:
        select_artist = spotify.artist(artist_uri)['name'] #used to check if artist entered is correct based on queried uri
        correct_artist = input("Is "+select_artist+" the artist you want to analyze? Enter 1 for yes, 0 for no. ")
        if correct_artist == "1":
            AudioAnalysis(artist_uri)
        else:
            print("Please try again with a more specific search and check for typos.") #exit if artist isn't correct
            sys.exit()

if __name__ == '__main__':
    main()