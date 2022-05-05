import os
import pytest 
from dotenv import load_dotenv

from app.spotify_service import SpotifyService
service = SpotifyService()


load_dotenv()

@pytest.mark.skipif(os.getenv("CI")=="true", reason="avoid issuing on the CI server") # skips this test on CI
def test_get_artist():
    assert service.get_artist("Taylor Swift") == "spotify:artist:06HL4z0CvFAxyc27GXpf02"

@pytest.mark.skipif(os.getenv("CI")=="true", reason="avoid issuing on the CI server") # skips this test on CI
def test_verifyartist():
    artist = service.verify_artist("spotify:artist:06HL4z0CvFAxyc27GXpf02") #artist will look like "Taylor Swift"
    assert isinstance(artist,str)

@pytest.mark.skipif(os.getenv("CI")=="true", reason="avoid issuing on the CI server") # skips this test on CI
def test_artist_albums():
    results = service.artist_albums("spotify:artist:06HL4z0CvFAxyc27GXpf02")
    assert isinstance(results,list)
    album = results[0] #album will look like this: ('1989', 'Released:', '2014-10-27', 'Total Tracks:', 13)
    assert len(album) == 5
    assert isinstance(album,tuple)

@pytest.mark.skipif(os.getenv("CI")=="true", reason="avoid issuing on the CI server") # skips this test on CI
def test_artist_top_tracks():
    results = service.artist_top_tracks("spotify:artist:06HL4z0CvFAxyc27GXpf02")
    assert isinstance(results,list)
    assert len(results) == 5
    track = results[0] #track will look like 'Ribs'
    assert isinstance(track,str)

@pytest.mark.skipif(os.getenv("CI")=="true", reason="avoid issuing on the CI server") # skips this test on CI
def test_artist_song_recs():
    results = service.artist_song_recommendations("spotify:artist:06HL4z0CvFAxyc27GXpf02")
    assert isinstance(results,list)
    songrec = results[0] #songrec will look like ('Adore You', 'by', 'Harry Styles')
    assert len(songrec) == 3
    assert isinstance(songrec,tuple)

@pytest.mark.skipif(os.getenv("CI")=="true", reason="avoid issuing on the CI server") # skips this test on CI
def test_artist_recs():
    results = service.artist_recs("spotify:artist:06HL4z0CvFAxyc27GXpf02")
    assert isinstance(results,list)
    artistrec = results[0] #artistrec will look like 'Taylor Swift'
    assert isinstance(artistrec,str)

@pytest.mark.skipif(os.getenv("CI")=="true", reason="avoid issuing on the CI server") # skips this test on CI
def test_get_characteristics():
    id = "spotify:track:51QEyJI5M7uyd8DOh9tqQY" #Buzzcut Season by Lorde
    results = service.get_characteristics(id)
    assert len(results) == 15
    assert isinstance(results, list)
    assert isinstance(results[4],int) #length
    assert isinstance(results[14],int) #time signature
    assert isinstance(results[6],float) #acousticness
    assert isinstance(results[1],str) #album

def test_dummy():
    assert 1 + 1 == 2