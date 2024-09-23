"ここでオブジェクトを定義します"
import pygame as pg
import datetime
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
        self.space = self.game.stage.map[self.y][self.x] #プレイヤーが現在いるマスの情報(0 or 1 or ...)
        self.count = 15 #次に移動するまでのフレーム数。実質的な移動速度は (count // speed) となる。
        self.past_x = self.x #動かす前のx
        self.past_y = self.y #動かす前のy
        self.now = pg.time.get_ticks() #現在の経過時間の取得
        self.last_move_time = 0 # 最初の初期化時、まだ移動していないので現在時刻に設定
        self.speed = 150  # 150ミリ秒（0.15秒）ごとに移動可能
    
    #フロア移動の際のxとyの移動
    def up_down(self): 
        if self.space % 2 == 0: 
            new_space = self.space + 1 
            self.y, self.x = tools.find_np_array_index(self.game.stage.map, new_space)
            self.past_y, self.past_x = self.y, self.x 
        else:
            new_space = self.space - 1 
            self.y, self.x = tools.find_np_array_index(self.game.stage.map, new_space)
            self.past_y, self.past_x = self.y, self.x  

    #プレイヤー操作
    def move(self):
        time_elapsed = self.now - self.last_move_time  # 前回の移動から経過した時間

        # 一定の時間が経過した場合に移動を行う
        if time_elapsed > self.speed: 
            keys = pg.key.get_pressed() 
            if keys[K_a] or keys[K_LEFT]: 
                self.past_x, self.past_y = self.x, self.y
                self.x -= 1 
            elif keys[K_d] or keys[K_RIGHT]: 
                self.past_x, self.past_y = self.x, self.y 
                self.x += 1 
            elif keys[K_w] or keys[K_UP]: 
                self.past_x, self.past_y = self.x, self.y 
                self.y -= 1 
            elif keys[K_s] or keys[K_DOWN]: 
                self.past_x, self.past_y = self.x, self.y
                self.y += 1 

            # 移動が発生した場合、移動時間をリセット
            self.last_move_time = self.now
    
        #移動先のマスに対する操作
        if self.game.stage.map[self.y][self.x] == 1: #壁のとき
            self.x, self.y = self.past_x, self.past_y
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
        #0が空白マス，1が壁，2がイベントマス, 3がスタートマス, 4以上の偶数が上階段, 5以上の奇数が下階段, -1がゴールマス
        color_list = {0:c.BLACK, 1:self.s.WALL_COLOR[self.floor], 2:c.ORANGE, 3:c.SKY_BLUE, -1:c.FOREST_GREEN}
        if number >3 and number%2 ==0:
            return c.PURPLE
        elif number >3 and number%2 == 1:
            return c.NAVY_BLUE
        return color_list[number]
