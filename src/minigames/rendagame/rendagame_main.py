import pygame as pg
from pygame.locals import *
from . import classes as cl
from . import consts as c

def main():
    game = cl.Control()
    state_dict = {c.START: cl.Start(),
                  c.PLAY: cl.Play(),
                  c.RESULT: cl.Result()}
    game.setup_status(state_dict, c.START)
    game.main()