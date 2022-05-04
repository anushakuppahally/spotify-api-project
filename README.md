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

Sign up for a Spotify developer's account and create a new app. Locate the Client ID and Client Secret for your app (i.e. `SPOTIPY_CLIENT_ID` and `SPOTIPY_CLIENT_SECRET`). Also, sign up for a SendGrid account, configure your account's email address (i.e. `SENDER_ADDRESS`), and obtain an API key (i.e. `SENDGRID_API_KEY`). Create a new file called .env and paste the following values inside, using your own credentials:

`SENDER_ADDRESS="_______________"`

`SENDGRID_API_KEY="_______________"`

`SPOTIPY_CLIENT_ID = '_______________'`

`SPOTIPY_CLIENT_SECRET = '_______________'`

## Usage


Get an email report that contains information about the artist, recommendations, and characteristics of their discography:

```sh
python -m app.music_report

```

## Testing

Run tests by using pytest. 

```
pytest
``` 