import pygame as pg
import sys, datetime, os
from pygame.locals import *     #pygameの定数
from .data import consts as c
from .data.maps import stage1 as s1
from . import tools,classes,state
from .minigames.rendagame import rendagame_main

stage_list = {1: s1}
floor_list = {1: "1F", 2: "2F", 3: "3F" , 4: "4F", 5: "5F"}

class Game():
    def __init__(self):
        #各変数の初期値設定
        self.state = "title"
        self.running = True #メインループ回すとき，この変数使うのが定番らしい．あまり気にしなくていい
        self.clock = pg.time.Clock() #時間オブジェクトの作成．fpsを管理するのに使う
        self.time_now = 0 #管理している今の時間．0はまだ管理している時間がない状態．
        self.current_screen = None #現在スクリーンに何を表示しているか
        self.current_stage = 1 #現在のステージ
        self.current_floor = 1 #現在のフロア
        self.s = stage_list[self.current_stage]
        self.time_limit = self.s.TIME_LIMIT #制限時間
        self.stage = classes.Stage(self) #Stageのインスタンスを作成
        self.player = classes.Player(self) #Playerのインスタンスを作成
        self.goal_flag = False
        
        pg.init() #おまじない．気にしなくていい
        self.screen = state.Screen()

    def exchange(self, point):
        return ord(point) - ord("A") +1

    
    def run(self):
        while self.running:
            if self.state == "title": #タイトル画面の描写
                self.current_screen = state.Title(self.screen)

            elif self.state == "stageSelect": #ステージセレクト画面の描写
                self.current_screen = state.StageSelect(self.screen)

            elif self.state == "game": #ゲーム画面の描写
                self.current_screen = state.GameScreen(self)
                #時間管理
                if self.time_now == 0: #管理する時間が未設定なら設定してあげる
                    self.time_now = pg.time.get_ticks() // 1000
                elif self.time_now - (pg.time.get_ticks() // 1000) != 0: #管理している時間と今の時間に差があったら
                    self.time_limit = self.time_limit - 1 #制限時間を1s減らす
                    self.time_now = pg.time.get_ticks() // 1000
                if self.time_limit == 0: #制限時間が0になったら
                    self.state = "gameover" #ゲームオーバー画面に移行
                if self.player.space > 3 and self.player.space % 2 == 0 and (self.player.past_x, self.player.past_y) != (self.player.x, self.player.y):
                    self.current_floor+=1
                    self.stage = classes.Stage(self) #Stageのマップを更新
                    self.player.up_down()
                elif self.player.space > 3 and self.player.space % 2 == 1 and (self.player.past_x, self.player.past_y) != (self.player.x, self.player.y):
                    self.current_floor-=1
                    self.stage = classes.Stage(self) #Stageのマップを更新
                    self.player.up_down()
                if (self.player.x, self.player.y) == (self.s.EVENT_X, self.exchange(self.s.EVENT_Y)) and self.player.space == 2 and (self.player.past_x, self.player.past_y) != (self.player.x, self.player.y):
                    self.state = "minigame"
            
            elif self.state == "minigame" and (self.player.past_x, self.player.past_y) != (self.player.x, self.player.y):
                self.player.past_x, self.player.past_y = self.player.x, self.player.y
                self.current_screen = None
                self.goal_flag = rendagame_main.main()
                pg.display.set_caption(c.TITLE_NAME)
                self.state = "game"

            elif self.state == "goalList": #目標確認画面の描写
                self.current_screen = state.MissionScreen(self)

            elif self.state == "gameover": #ゲームオーバー画面の描写
                self.current_screen = state.GameOver(self.screen)

            pg.display.update() #今までの変更を全部反映させる

            #移動処理
            if self.state == "game":
                self.player.now = pg.time.get_ticks()
                self.player.move()

            #イベント処理
            for event in pg.event.get():
                if event.type == QUIT: #ウィンドウが閉じられたら終了
                    pg.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if self.state == "title": #タイトル画面なら反応
                        if self.current_screen.start_button.collidepoint(event.pos): #ボタンがクリックされたら
                            self.state = "stageSelect" #ステージセレクト画面に移行

                    elif self.state == "stageSelect": #ステージセレクト画面なら反応
                        if self.current_screen.stage1_button.collidepoint(event.pos):
                            self.state = "game"
                            
                    elif self.state == "game": #ゲーム画面なら反応
                        if self.current_screen.goal_button.collidepoint(event.pos): #ボタンがクリックされたら
                            self.state = "goalList" #目標確認画面に移行

                    elif self.state == "goalList": #目標確認画面なら反応
                        if self.current_screen.back_button.collidepoint(event.pos): #ボタンがクリックされたら
                            self.state = "game" #ゲーム画面に移行
                    
                    elif self.state == "gameover":
                        if self.current_screen.back_button.collidepoint(event.pos):
                            self.__init__()
                            self.state = "stageSelect"
                            """
                            self.time_limit = self.s.TIME_LIMIT
                            self.time_now = 0
                            self.goal_flag = False
                            self.stage = classes.Stage(self) #Stageのインスタンスを作成
                            self.player = classes.Player(self) #Playerのインスタンスを作成
                            self.state = "stageSelect"
                            """
                            
            
            self.clock.tick(120) #120fps
            pg.display.update() #今までの変更を全部反映させる
            
                            
#メイン関数
def main():
    game = Game()
    game.run()

