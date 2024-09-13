import pytest
from src.data.maps import stage1

def test_practice():
    assert stage1.PLAYER_INIT["1F"] == (2,2), "(2,2)じゃないよ"