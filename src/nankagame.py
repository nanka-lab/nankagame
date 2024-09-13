import pygame as pg
import sys, datetime, os
from pygame.locals import *     #pygameの定数
from . import tools,classes,state

class Game():
    def __init__(self):
        #各変数の初期値設定
        self.stage = classes.Stage() #Stageのインスタンスを作成
        self.player = classes.Player() #Playerのインスタンスを作成
        self.state = "title"
        self.running = True #メインループ回すとき，この変数使うのが定番らしい．あまり気にしなくていい
        self.clock = pg.time.Clock() #時間オブジェクトの作成．fpsを管理するのに使う
        self.time = 0 #管理している時間．0はまだ管理している時間がない状態．
        self.time_limit = 20 #制限時間
        self.current_screen = None

        pg.init() #おまじない．気にしなくていい
        self.screen = state.Screen(self.stage)
        self.stage.create_stage() #ステージを管理する配列を作成
    
    def run(self):
        while self.running:
            if self.state == "title": #タイトル画面の描写
                self.current_screen = state.Title(self.screen)

            elif self.state == "stageSelect": #ステージセレクト画面の描写
                self.current_screen = state.StageSelect(self.screen)

            elif self.state == "game": #ゲーム画面の描写
                self.current_screen = state.GameScreen(self)

            elif self.state == "goalList": #目標確認画面の描写
                self.current_screen = state.MissionScreen(self.screen)

            elif self.state == "gameover": #ゲームオーバー画面の描写
                self.current_screen = state.GameOver(self.screen)

            pg.display.update() #今までの変更を全部反映させる

            #時間管理
            now = datetime.datetime.now() #現在時刻の取得
            if self.time == 0: #管理する時間が未設定なら設定してあげる
                self.time = now
            elif self.time.second - now.second != 0: #管理している時間と今の時間に差があったら
                self.time_limit = self.time_limit - 1 #制限時間を1s減らす
                self.time = now
            if self.time_limit == 0: #制限時間が0になったら
                self.state = "gameover" #ゲームオーバー画面に移行

            #イベント処理
            for event in pg.event.get():
                if event.type == QUIT: #ウィンドウが閉じられたら終了
                    pg.quit()
                    sys.exit()
                    
                elif event.type == KEYDOWN: #移動キー押されたら動こう
                    if self.state == "game": #ゲーム画面ならプレイヤー移動
                        self.player.move(event.key, self.stage.stage)
                        
                elif event.type == MOUSEBUTTONDOWN:
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

            self.clock.tick(60) #60fps
                            
#メイン関数
def main():
    game = Game()
    game.run()
main()

