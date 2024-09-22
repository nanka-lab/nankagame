import pygame as pg
from pygame.locals import *
from . import classes as cl
from . import consts as c
from . import setup

def main():
    pg.init()
    pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP, pg.QUIT])
    pg.display.set_caption(c.GAME_TITLE)
    SCREEN = pg.display.set_mode(c.SCREEN_SIZE)
    game = cl.Control()
    state_dict = {c.START: cl.Start(),
                  c.PLAY: cl.Play(),
                  c.COUNT_DOWN: cl.Count_down(),
                  c.RESULT: cl.Result()}
    game.setup_status(state_dict, c.START)
    result = game.main()
    return result