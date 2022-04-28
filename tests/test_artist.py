from app.artist_analysis import GetArtist

def test_artist():
    assert GetArtist("Taylor Swift") == "spotify:artist:06HL4z0CvFAxyc27GXpf02"