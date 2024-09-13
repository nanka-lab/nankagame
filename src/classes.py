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
        self.speed = 1 #移動速度。
        self.count = 15 #次に移動するまでのフレーム数。実質的な移動速度は (count // speed) となる。
        self.a_count = 0 #[wasd]_count はそのキーを押して移動してからの現在のフレーム数。別のキーを押すとリセットされるが、時間を置いて同じキーを押す場合のリセットは未実装。
        self.d_count = 0
        self.w_count = 0
        self.s_count = 0
        self.past_x = None #動かす前のx
        self.past_y = None #動かす前のy


    
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
        xOld, yOld = self.x, self.y #移動前のプレイヤーの場所を管理する変数
        keys = pg.key.get_pressed() #それぞれのキーについて押されているかをブール値で表したもの

        #押されたキーに対する操作
        if keys[K_a] or keys[K_LEFT]:
            if self.d_count + self.w_count + self.s_count:
                self.a_count = 0
                self.d_count = 0
                self.w_count = 0
                self.s_count = 0
            self.a_count -= self.speed
        elif keys[K_d] or keys[K_RIGHT]:
            if self.a_count + self.w_count + self.s_count:
                self.a_count = 0
                self.d_count = 0
                self.w_count = 0
                self.s_count = 0
            self.d_count -= self.speed
        elif keys[K_w] or keys[K_UP]:
            if self.a_count + self.d_count + self.s_count:
                self.a_count = 0
                self.d_count = 0
                self.w_count = 0
                self.s_count = 0
            self.w_count -= self.speed
        elif keys[K_s] or keys[K_DOWN]:
            if self.a_count + self.d_count + self.w_count:
                self.a_count = 0
                self.d_count = 0
                self.w_count = 0
                self.s_count = 0
            self.s_count -= self.speed

        if self.a_count < 0:
            self.past_y, self.past_x = self.y, self.x
            self.x -= 1
            self.a_count = self.count - 1
        elif self.d_count < 0:
            self.past_y, self.past_x = self.y, self.x
            self.x += 1
            self.d_count = self.count - 1
        elif self.w_count < 0:
            self.past_y, self.past_x = self.y, self.x
            self.y -= 1
            self.w_count = self.count - 1
        elif self.s_count < 0:
            self.past_y, self.past_x = self.y, self.x
            self.y += 1
            self.s_count = self.count - 1
    
        #移動先のマスに対する操作
        if self.game.stage.map[self.y][self.x] == 1: #壁のとき
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