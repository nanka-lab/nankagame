"ここでオブジェクトを定義します"
import pygame as pg
from pygame.locals import *
from .data import consts as c
from .data.maps import stage1 as s1

class Player():
    def __init__(self):
        #各変数の初期値設定
        self.x = s1.PLAYER_INIT["1F"][0] #x, y はプレイヤーの位置。とりあえず左上のマスにしとく。
        self.y = s1.PLAYER_INIT["2F"][1]

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

class Stage():
    def __init__(self):
        #各変数の初期値設定
        self.grid_size = 40 #1マスの長さ
        self.height = 9  #ステージの行数
        self.width = 11 #ステージの列数
        self.height_blank = 150 #縦の空白部分
        self.width_blank = 200 #横の空白部分
        self.stage = [] #ステージを管理する配列
        #0が空白マス，1が壁，2がイベントマス,3がスタートマス "player"がプレイヤーの色
        self.colors = {0:c.BLACK, 1:c.FOREST_GREEN, 2:c.ORANGE, 3:c.ORANGE, "player":c.PLAYER_COLOR} #順番にblack、FORESTGREEN、orange、blue
    
    # ステージ生成
    def create_stage(self):
        #ステージの配列の作成
        self.stage = s1.MAP["1F"]

        """
        理想はstage_createの引数に階層とか入れることでそのステージの配列を返すような関数を作りたい
        別に作っといてモジュールとしてimportするのもアリかもね
        ちなみにこの配列形式を採用した理由としては，視覚的に見やすくて簡単に変更出来るからなんだけど,
        ステージが大きくなればなるほど大変になるので要検討．
        """
