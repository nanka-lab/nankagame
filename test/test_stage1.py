import pytest
#from src.data.maps import stage1
from src.minigames.rendagame import rendagame_main

def test_renda():
    rendagame_main.main()

#def test_practice():
    assert stage1.PLAYER_INIT == (1,1), "(1,1)じゃないよ"