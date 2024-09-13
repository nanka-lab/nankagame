"ここでオブジェクトを定義します"
import pygame as pg
from pygame.locals import *

class Player():
    def __init__(self):
        #各変数の初期値設定
        self.x = 1 #x, y はプレイヤーの位置。とりあえず左上のマスにしとく。
        self.y = 1
        self.speed = 1 #移動速度。
        self.count = 15 #次に移動するまでのフレーム数。実質的な移動速度は (count // speed) となる。
        self.a_count = 0 #[wasd]_count はそのキーを押して移動してからの現在のフレーム数。別のキーを押すとリセットされるが、時間を置いて同じキーを押す場合のリセットは未実装。
        self.d_count = 0
        self.w_count = 0
        self.s_count = 0

    #プレイヤー操作
    def move(self, stage):
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
            self.x -= 1
            self.a_count = self.count - 1
        elif self.d_count < 0:
            self.x += 1
            self.d_count = self.count - 1
        elif self.w_count < 0:
            self.y -= 1
            self.w_count = self.count - 1
        elif self.s_count < 0:
            self.y += 1
            self.s_count = self.count - 1
    
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
        #0が空白マス，1が壁，2がイベントマス, "player"がプレイヤーの色
        self.colors = {0:(0, 0, 0), 1:(115, 66, 41), 2:(233, 168, 38), "player":(0, 0, 255)} #順番にblack、brown、orange、blue
    
    # ステージ生成
    def create_stage(self):
        #ステージの配列の作成
        self.stage = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                      [1, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 0, 1],
                      [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                      [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                      [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                      [1, 0, 0, 1, 0, 2, 0, 0, 1, 1, 1, 0, 1],
                      [1, 0, 0, 1, 0, 0, 0, 0, 1, 2, 1, 0, 1],
                      [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1],
                      [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                      [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                      [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

        """
        理想はstage_createの引数に階層とか入れることでそのステージの配列を返すような関数を作りたい．
        別に作っといてモジュールとしてimportするのもアリかもね．
        ちなみにこの配列形式を採用した理由としては，視覚的に見やすくて簡単に変更出来るからなんだけど,
        ステージが大きくなればなるほど大変になるので要検討．
        """
