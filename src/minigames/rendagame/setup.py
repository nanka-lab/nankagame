import pygame as pg
from pygame.locals import *
from . import consts as c


pg.init()
pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP, pg.QUIT])
pg.display.set_caption(c.GAME_TITLE)
SCREEN = pg.display.set_mode(c.SCREEN_SIZE)

