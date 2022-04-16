# Spotify App (Python)

## Installation 

Create a copy of this and clone/download to your local computer. Then, navigate there from the command-line. 

```sh
cd ~/Desktop/spotify-api-project/
```

Use Anaconda to create and activate a new virtual environment, perhaps called "spotify-env":

```sh
conda create -n spotify-env python=3.8
conda activate spotify-env
```

Then, within an active virtual environment, install package dependencies:

```sh
pip install -r requirements.txt
```

## Configuration

Sign up for a Spotify developer's account and create a new app. Locate the Client ID and Client Secret for your app. Also, sign up for a SendGrid account, configure your account's email address (i.e. `SENDER_EMAIL_ADDRESS`), and obtain an API key (i.e. `SENDGRID_API_KEY`). Create a new file called .env and paste the following values inside, using your own credentials:

SENDER_ADDRESS="____"
SENDGRID_API_KEY="____"
SPOTIPY_CLIENT_ID = '____'
SPOTIPY_CLIENT_SECRET = '____'

## Usage

Get a report on an entered artist's discography and receive recommendations based on this artist. 

```sh
python -m app.artist_analysis

```