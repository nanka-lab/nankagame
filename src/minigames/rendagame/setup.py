import pygame as pg
from pygame.locals import *
import os
from . import consts as c
from . import classes as cl


pg.init()
pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP, pg.QUIT])
pg.display.set_caption(c.GAME_TITLE)
SCREEN = pg.display.set_mode(c.SCREEN_SIZE)
#画像取得

GFX = cl.load_all_gfx(os.path.join("assets", "image"))

