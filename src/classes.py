"ここでオブジェクトを定義します"
import pygame as pg
from pygame.locals import *
from .data import consts as c
from . import tools
from .data.maps import stage1 as s1

stage_list = {1: s1}
floor_list = {1: "1F", 2: "2F", 3: "3F" , 4: "4F", 5: "5F"}

"""座標系

          →x
      ↓y
"""


class Player():
    def __init__(self, game):
        self.s=stage_list[game.current_stage] #sはimportするファイルのエイリアスを保持する変数
        self.floor = floor_list[game.current_floor] #floorは階数の文字列を保持する変数
        self.game = game
        #各変数の初期値設定
        self.x, self.y = self.s.PLAYER_INIT #x, y はプレイヤーの位置。とりあえず左上のマスにしとく。
        self.space = self.game.stage.map[self.y][self.x]
    
    #フロア移動の際のxとyの移動
    def up_down(self):
        if self.space % 2 == 0:
            new_space = self.space + 1
            self.y, self.x = tools.find_np_array_index(self.game.stage.map, new_space)
        else:
            new_space = self.space - 1
            self.y, self.x = tools.find_np_array_index(self.game.stage.map, new_space)

    #プレイヤー操作
    def move(self, key, stage):
        xOld, yOld = self.x, self.y #移動前のプレイヤーの場所を管理する変数
    
        #押されたキーに対する操作
        if key == K_a or key == K_LEFT:
            self.x -= 1
        elif key == K_d or key == K_RIGHT:
            self.x += 1
        elif key == K_w or key == K_UP:
            self.y -= 1
        elif key == K_s or key == K_DOWN:
            self.y += 1
    
        #移動先のマスに対する操作
        if stage[self.y][self.x] == 1: #壁のとき
            self.x, self.y = xOld, yOld
        self.space = self.game.stage.map[self.y][self.x]


class Stage():
    def __init__(self, game):
        self.s=stage_list[game.current_stage] #sはimportするファイルのエイリアスを保持する変数
        self.floor = floor_list[game.current_floor] #floorは階数の文字列を保持する変数

        #各変数の初期値設定
        self.grid_size = self.s.GRID_SIZE[self.floor] #1マスの長さ
        self.row_number = self.s.ROW_NUMBER[self.floor] #ステージの行数
        self.column_number = self.s.COLUMN_NUMBER[self.floor] #ステージの列数
        self.height_blank = self.s.HEIGHT_BLANK[self.floor] #縦の空白部分
        self.width_blank = self.s.WIDTH_BLANK[self.floor] #横の空白部分
        self.map = self.s.MAP[self.floor]

    #マスの色を取得する関数
    def get_color(self, number):
        #0が空白マス，1が壁，2がイベントマス, 3がスタートマス, 4以上の偶数が上階段, 5以上の奇数が下階段
        color_list = {0:c.BLACK, 1:self.s.WALL_COLOR[self.floor], 2:c.ORANGE, 3:c.SKY_BLUE}
        if number >3 and number%2 ==0:
            return c.PURPLE
        elif number >3 and number%2 == 1:
            return c.NAVY_BLUE
        return color_list[number]