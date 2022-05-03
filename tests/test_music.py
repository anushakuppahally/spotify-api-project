from app.music_report import GetCharacteristics
from app.music_report import AudioAnalysis

id = "spotify:track:51QEyJI5M7uyd8DOh9tqQY" #Buzzcut Season by Lorde

def test_getcharacteristics():
    results = GetCharacteristics(id)
    assert len(results) == 15
    assert isinstance(results, list)
    assert isinstance(results[4],int) #length
    assert isinstance(results[14],int) #time signature
    assert isinstance(results[6],float) #acousticness
    assert isinstance(results[1],str) #album