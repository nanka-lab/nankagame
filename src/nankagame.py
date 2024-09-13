import pygame as pg
import sys, datetime, os
from pygame.locals import *     #pygameの定数まとめ
from . import tools,classes

#フォントファイルのパスを取得
root_dir = os.path.abspath(tools.find_dir_path("nankagame")) #リポジトリのパスを取得
font_path = os.path.join(root_dir, "assets", "fonts", "ヒラギノ角ゴシック W1.ttc") #フォントファイルのパスを取得




class Game():
    def __init__(self):
        #各変数の初期値設定
        self.stage = classes.Stage() #Stageのインスタンスを作成
        self.player = classes.Player() #Playerのインスタンスを作成
        self.state = "title"
        self.running = True #メインループ回すとき，この変数使うのが定番らしい．あまり気にしなくていい
        self.clock = pg.time.Clock() #時間オブジェクトの作成．fpsを管理するのに使う
        self.time = 0 #管理している時間．0はまだ管理している時間がない状態．
        self.timeLimit = 360 #制限時間

        #各色の定義       R    G    B
        self.black  = (  0,   0,   0)
        self.white  = (255, 255, 255)
        self.red    = (255,   0,   0)
        self.green  = (  0, 255,   0)
        self.blue   = (  0,   0, 255)
        self.brown  = (115,  66,  41)
        self.orange = (233, 168,  38)
        self.gray   = (127, 127, 127)

        #ウィンドウジオメトリ
        self.height = (self.stage.height + 2) * self.stage.grid_size + self.stage.height_blank + (self.stage.height_blank - 60) #ウィンドウの高さ．式キモいけど見逃して．
        self.width = (self.stage.width + 2) * self.stage.grid_size + self.stage.width_blank * 2               #ウィンドウの長さ．同上

        pg.init() #おまじない．気にしなくていい
        pg.display.set_caption("なんかげーむ") #ウィンドウの名前を指定できます
        self.screen = pg.display.set_mode((self.width, self.height)) #ウィンドウ作成
        self.stage.create_stage() #ステージを管理する配列を作成
    
    def run(self):
        while self.running:
            if self.state == "title": #タイトル画面の描写
                self.screen.fill(self.black) #背景を全部黒にして

                #タイトル作ります
                titleFont = pg.font.Font(font_path, 74) #タイトルを描画するフォントを設定
                titleText = titleFont.render("なんかげーむ", True, self.white)
                titleTextRect = titleText.get_rect(center = (self.width // 2, self.height // 2 - 150))
                self.screen.blit(titleText, titleTextRect)

                #スタートボタン作ります
                startButton = pg.draw.rect(self.screen, self.green, (self.width // 2 - 100, self.height // 2, 200, 50))
                startButtonFont = pg.font.Font(font_path, 28) #ボタンのフォント設定
                startButtonText = startButtonFont.render("げーむすたーと", True, self.black)
                startButtonTextRect = startButtonText.get_rect(center = (self.width // 2, self.height // 2 + 25))
                self.screen.blit(startButtonText, startButtonTextRect)

            elif self.state == "stageSelect": #ステージセレクト画面の描写
                self.screen.fill(self.gray) #背景を全部灰色にする
                stageButtonFont = pg.font.Font(font_path, 20) #フォント設定

                #ステージ1のボタンの描写
                stage1Button = pg.draw.rect(self.screen, self.white,
                                                (30, 30, (self.width - 120) // 3, self.height - 60))
                stage1ButtonText = stageButtonFont.render("今はここしか選べないよ", True, self.black)
                stage1ButtonTextRect = stage1ButtonText.get_rect(center =
                                                                (30 + ((self.width - 120) // 3) // 2,
                                                                (30 + (self.height - 60) // 2)))
                self.screen.blit(stage1ButtonText, stage1ButtonTextRect)

                #ステージ2のボタンの描写
                stage2Button = pg.draw.rect(self.screen, self.white,
                                                (60 + (self.width - 120) // 3, 30,
                                                 (self.width - 120) // 3, self.height - 60))
                stage2ButtonText = stageButtonFont.render("選べないよ", True, self.black)
                stage2ButtonTextRect = stage2ButtonText.get_rect(center =
                                                                (60 + 3 * ((self.width - 120) // 3) // 2,
                                                                (30 + (self.height - 60) // 2)))
                self.screen.blit(stage2ButtonText, stage2ButtonTextRect)

                #ステージ3のボタンの描写
                stage3Button = pg.draw.rect(self.screen, self.white,
                                                (90 + 2 * (self.width - 120) // 3, 30,
                                                 (self.width - 120) // 3, self.height - 60))
                stage3ButtonText = stageButtonFont.render("選べないよ", True, self.black)
                stage3ButtonTextRect = stage3ButtonText.get_rect(center =
                                                                (90 + 5 * ((self.width - 120) // 3) // 2,
                                                                (30 + (self.height - 60) // 2)))
                self.screen.blit(stage3ButtonText, stage3ButtonTextRect)
                

            elif self.state == "game": #ゲーム画面の描写
                self.screen.fill(self.gray) #背景を全部灰色にする
                #ステージ部分の背景を白にする．これも式キモいけど許して
                pg.draw.rect(self.screen, self.white, (self.stage.width_blank, self.stage.height_blank, (self.stage.width + 2) * self.stage.grid_size, (self.stage.height + 2) * self.stage.grid_size))

                #ステージを描画する
                stageFont = pg.font.Font(font_path, 25) #座標を描画するフォントの設定

                for y in range(self.stage.height + 2):
                    for x in range(self.stage.width + 2):
                        state = self.stage.stage[y][x] #マスの状態を管理する変数

                        if state == 0: #マスが空白なら枠線作る
                            pg.draw.rect(self.screen, self.stage.colors[state],
                                             (x * self.stage.grid_size + self.stage.width_blank, y * self.stage.grid_size + self.stage.height_blank, self.stage.grid_size, self.stage.grid_size), 1)
                        elif state == 1: #マスが壁なら壁を描写する
                            pg.draw.rect(self.screen, self.stage.colors[state],
                                             (x * self.stage.grid_size + self.stage.width_blank, y * self.stage.grid_size + self.stage.height_blank, self.stage.grid_size, self.stage.grid_size))
                        elif state == 2: #マスがイベントマスならそれも描く描くしかじか
                            pg.draw.rect(self.screen, self.stage.colors[state],
                                             (x * self.stage.grid_size + self.stage.width_blank, y * self.stage.grid_size + self.stage.height_blank, self.stage.grid_size, self.stage.grid_size))

                        #x軸の座標の描画．式キモめ
                        if y == 0 and x >= 1 and x <= self.stage.width:
                            xText = stageFont.render(f"{x}", True, self.white)
                            xTextRect = xText.get_rect(center = (
                                (x * self.stage.grid_size + self.stage.width_blank) + self.stage.grid_size // 2 - 1, (y * self.stage.grid_size + self.stage.height_blank) + self.stage.grid_size // 2))
                            self.screen.blit(xText, xTextRect)

                        #y軸の座標の描画．式キモめ2
                        if x == 0 and y >= 1 and y <= self.stage.height:
                            yText = stageFont.render(f"{chr(64+y)}", True, self.white)
                            yTextRect = yText.get_rect(center = (
                                (x * self.stage.grid_size + self.stage.width_blank) + self.stage.grid_size // 2, (y * self.stage.grid_size + self.stage.height_blank) + self.stage.grid_size // 2))
                            self.screen.blit(yText, yTextRect)

                #プレイヤーを描画する．これも式キモいね，ごめんね，頑張ってね
                pg.draw.circle(self.screen, self.stage.colors["player"],
                                   (self.player.x * self.stage.grid_size + self.stage.width_blank + self.stage.grid_size // 2, self.player.y * self.stage.grid_size + self.stage.height_blank + self.stage.grid_size // 2), 15)

                #時間管理
                now = datetime.datetime.now() #現在時刻の取得
                if self.time == 0: #管理する時間が未設定なら設定してあげる
                    self.time = now
                elif self.time.second - now.second != 0: #管理している時間と今の時間に差があったら
                    self.timeLimit = self.timeLimit - 1 #制限時間を1s減らす
                    self.time = now
                if self.timeLimit == 0: #制限時間が0になったら
                    self.state = "gameover" #ゲームオーバー画面に移行

                #メニューの描画
                pg.draw.rect(self.screen, self.white, (0, 0, self.width, 60)) #メニューの背景を白色に
                menuFont = pg.font.Font(font_path, 40) #メニューのフォントの設定
                menuText = menuFont.render(f"ステージ1：1F   フロア数：5   制限時間：{self.timeLimit}s", True, self.black)
                self.screen.blit(menuText, (22, 10)) #いい感じのところに配置

                #目標確認ボタン作ります
                goalButton = pg.draw.rect(self.screen, self.black, (self.width - 90, 70, 80, 40))
                goalButtonFont = pg.font.Font(font_path, 28) #ボタンのフォント設定
                goalButtonText = goalButtonFont.render("目標", True, self.white)
                goalButtonTextRect = goalButtonText.get_rect(center = (self.width - 90 + 80 // 2, 70 + 40 // 2))
                self.screen.blit(goalButtonText, goalButtonTextRect)

            elif self.state == "goalList": #目標確認画面の描写
                self.screen.fill(self.gray) #背景を全部灰色にする

                #目標確認リスト作ります
                goalList = pg.draw.rect(self.screen, self.white, (50, 50, self.width - 100, self.height - 100))
                goalListFont = pg.font.Font(font_path, 50) #フォント設定
                goalListText = goalListFont.render("ここでデータベース班の出番だ！", True, self.black)
                goalListTextRect = goalListText.get_rect(center = (self.width // 2, self.height // 2))
                self.screen.blit(goalListText, goalListTextRect)

                #戻るボタンを作ります
                backButton = pg.draw.rect(self.screen, self.black, (10, 10, 60, 30))
                backButtonFont = pg.font.Font(font_path, 25) #フォント設定
                backButtonText = backButtonFont.render("戻る", True, self.white)
                backButtonTextRect = backButtonText.get_rect(center = (10 + 60 // 2, 10 + 30 // 2))
                self.screen.blit(backButtonText, backButtonTextRect)

            elif self.state == "gameover": #ゲームオーバー画面の描写
                self.screen.fill(self.black) #背景を真っ黒にする
                gameoverFont = pg.font.Font(font_path, 50) #フォント設定
                gameoverText = gameoverFont.render("げーむおーばー", True, self.red)
                gameoverTextRect = gameoverText.get_rect(center = (self.width // 2, self.height // 2))
                self.screen.blit(gameoverText, gameoverTextRect)

            pg.display.update() #今までの変更を全部反映させる

            #イベント処理
            for event in pg.event.get():
                if event.type == QUIT: #ウィンドウが閉じられたら終了
                    pg.quit()
                    sys.exit()
                    
                elif event.type == KEYDOWN: #移動キー押されたら動こう
                    if self.state == "game": #ゲーム画面ならプレイヤー移動
                        pass #self.player.move(event.key, self.stage.stage)
                        
                elif event.type == MOUSEBUTTONDOWN:
                    if self.state == "title": #タイトル画面なら反応
                        if startButton.collidepoint(event.pos): #ボタンがクリックされたら
                            self.state = "stageSelect" #ステージセレクト画面に移行

                    elif self.state == "stageSelect": #ステージセレクト画面なら反応
                        if stage1Button.collidepoint(event.pos):
                            self.state = "game"
                            
                    elif self.state == "game": #ゲーム画面なら反応
                        if goalButton.collidepoint(event.pos): #ボタンがクリックされたら
                            self.state = "goalList" #目標確認画面に移行
                            
                    elif self.state == "goalList": #目標確認画面なら反応
                        if backButton.collidepoint(event.pos): #ボタンがクリックされたら
                            self.state = "game" #ゲーム画面に移行
            self.player.move(self.stage.stage)

            self.clock.tick(60) #60fps
                            
#メイン関数
def main():
    game = Game()
    game.run()
main()

