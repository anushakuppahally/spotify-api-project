from app.artist_analysis import GetArtist
from app.artist_analysis import ArtistAlbums
from app.artist_analysis import ArtistTopTracks
from app.artist_analysis import ArtistSongRecommendations
from app.artist_analysis import ArtistRecs

import os
import pytest 
from dotenv import load_dotenv


load_dotenv()

@pytest.mark.skipif(os.getenv("CI")=="true", reason="avoid issuing on the CI server") # skips this test on CI
def test_getartist():
    assert GetArtist("Taylor Swift") == "spotify:artist:06HL4z0CvFAxyc27GXpf02"

@pytest.mark.skipif(os.getenv("CI")=="true", reason="avoid issuing on the CI server") # skips this test on CI
def test_artistalbums():
    results = ArtistAlbums("spotify:artist:06HL4z0CvFAxyc27GXpf02")
    assert isinstance(results,list)
    album = results[0] #album will look like this: ('1989', 'Released:', '2014-10-27', 'Total Tracks:', 13)
    assert len(album) == 5
    assert isinstance(album,tuple)

@pytest.mark.skipif(os.getenv("CI")=="true", reason="avoid issuing on the CI server") # skips this test on CI
def test_artisttoptracks():
    results = ArtistTopTracks("spotify:artist:06HL4z0CvFAxyc27GXpf02")
    assert isinstance(results,list)
    assert len(results) == 5
    track = results[0] #track will look like 'Ribs'
    assert isinstance(track,str)

@pytest.mark.skipif(os.getenv("CI")=="true", reason="avoid issuing on the CI server") # skips this test on CI
def test_artistsongrecs():
    results = ArtistSongRecommendations("spotify:artist:06HL4z0CvFAxyc27GXpf02")
    assert isinstance(results,list)
    songrec = results[0] #songrec will look like ('Adore You', 'by', 'Harry Styles')
    assert len(songrec) == 3
    assert isinstance(songrec,tuple)

@pytest.mark.skipif(os.getenv("CI")=="true", reason="avoid issuing on the CI server") # skips this test on CI
def test_artistrecs():
    results = ArtistRecs("spotify:artist:06HL4z0CvFAxyc27GXpf02")
    assert isinstance(results,list)
    artistrec = results[0] #artistrec will look like 'Taylor Swift'
    assert isinstance(artistrec,str)

def test_dummy():
    assert 1 + 1 == 2