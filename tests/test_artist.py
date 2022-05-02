from app.artist_analysis import GetArtist
from app.artist_analysis import ArtistMusic
from app.artist_analysis import ArtistRecommendations

def test_getartist():
    assert GetArtist("Taylor Swift") == "spotify:artist:06HL4z0CvFAxyc27GXpf02"

def test_artistmusic():
    results = ArtistMusic("spotify:artist:06HL4z0CvFAxyc27GXpf02")
    assert isinstance(results,list)
    album = results[1] #album will look like this: ('1989', 'Released:', '2014-10-27', 'Total Tracks:', 13))
    assert len(album) == 5
    assert isinstance(album,tuple)

def test_artistrecommendations():
    results = ArtistRecommendations("spotify:artist:06HL4z0CvFAxyc27GXpf02")
    assert isinstance(results,list)
    songrec = results[1] #songrec will look like ('Adore You', 'by', 'Harry Styles')
    assert len(songrec) == 3
    assert isinstance(songrec,tuple)