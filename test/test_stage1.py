import pytest
from src.data.maps import stage1

def test_practice():
    print(stage1.PLAYER_START_X)
    assert stage1.PLAYER_START_X == 1, "1じゃないよ"
    assert stage1.PLAYER_START_X >= 1, "1以上じゃないよ"
    assert stage1.PLAYER_START_X < 1, "1未満じゃないよ"
    assert stage1.PLAYER_START_X == 3, "3じゃないよ"
