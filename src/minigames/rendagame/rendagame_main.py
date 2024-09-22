import pygame as pg
from pygame.locals import *
import os
from . import setup
from . import classes as cl
from . import consts as c


def main():
    pg.init()
    pg.mixer.init()
    pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP, pg.QUIT])
    pg.display.set_caption(c.GAME_TITLE)
    SCREEN = pg.display.set_mode(c.SCREEN_SIZE)
    pg.mixer.music.load(setup.MUSIC["shining_star"])
    pg.mixer.music.play(loops = -1, start = 0.0, fade_ms = 0)
    game = cl.Control()
    state_dict = {c.START: cl.Start(),
                  c.PLAY: cl.Play(),
                  c.COUNT_DOWN: cl.Count_down(),
                  c.RESULT: cl.Result()}
    game.setup_status(state_dict, c.START)
    result = game.main()
    return result