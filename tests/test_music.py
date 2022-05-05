from app.music_report import GetCharacteristics

import os
import pytest
from dotenv import load_dotenv

load_dotenv()



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