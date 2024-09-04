import pygame, sys, datetime
from pygame.locals import *

class Player():
    def __init__(self):
        #各変数の初期値設定
        self.x = 1 #x, y はプレイヤーの位置。とりあえず左上のマスにしとく。
        self.y = 1

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
        self.gridSize = 40 #1マスの長さ
        self.height = 9  #ステージの行数
        self.width = 11 #ステージの列数
        self.heightBlank = 150 #縦の空白部分
        self.widthBlank = 200 #横の空白部分
        self.stage = [] #ステージを管理する配列
        #0が空白マス，1が壁，2がイベントマス, "player"がプレイヤーの色
        self.colors = {0:(0, 0, 0), 1:(115, 66, 41), 2:(233, 168, 38), "player":(0, 0, 255)} #順番にblack、brown、orange、blue
    
    # ステージ生成
    def createStage(self):
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

class Game():
    def __init__(self):
        #各変数の初期値設定
        self.stage = Stage() #Stageのインスタンスを作成
        self.player = Player() #Playerのインスタンスを作成
        self.state = "title"
        self.running = True #メインループ回すとき，この変数使うのが定番らしい．あまり気にしなくていい
        self.clock = pygame.time.Clock() #時間オブジェクトの作成．fpsを管理するのに使う
        self.time = 0 #管理している時間．0はまだ管理している時間がない状態．
        self.timeLimit = 360 #制限時間

        #各色の定義
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.brown = (115, 66, 41)
        self.orange = (233, 168, 38)
        self.gray = (127, 127, 127)
        self.height = (self.stage.height + 2) * self.stage.gridSize + self.stage.heightBlank + (self.stage.heightBlank - 60) #ウィンドウの高さ．式キモいけど見逃して．
        self.width = (self.stage.width + 2) * self.stage.gridSize + self.stage.widthBlank * 2               #ウィンドウの長さ．同上

        pygame.init() #おまじない．気にしなくていい
        pygame.display.set_caption("なんかげーむ") #ウィンドウの名前を指定できます
        self.screen = pygame.display.set_mode((self.width, self.height)) #ウィンドウ作成
        self.stage.createStage() #ステージを管理する配列を作成
    
    def run(self):
        while self.running:
            if self.state == "title": #タイトル画面の描写
                self.screen.fill(self.black) #背景を全部黒にして

                #タイトル作ります
                titleFont = pygame.font.SysFont("ヒラキノ角コシックw1", 74) #タイトルを描画するフォントを設定
                titleText = titleFont.render("なんかげーむ", True, self.white)
                titleTextRect = titleText.get_rect(center = (self.width // 2, self.height // 2 - 150))
                self.screen.blit(titleText, titleTextRect)

                #スタートボタン作ります
                startButton = pygame.draw.rect(self.screen, self.green, (self.width // 2 - 100, self.height // 2, 200, 50))
                startButtonFont = pygame.font.SysFont("ヒラキノ角コシックw1", 28) #ボタンのフォント設定
                startButtonText = startButtonFont.render("げーむすたーと", True, self.black)
                startButtonTextRect = startButtonText.get_rect(center = (self.width // 2, self.height // 2 + 25))
                self.screen.blit(startButtonText, startButtonTextRect)

            elif self.state == "stageSelect": #ステージセレクト画面の描写
                self.screen.fill(self.gray) #背景を全部灰色にする
                stageButtonFont = pygame.font.SysFont("ヒラキノ角コシックw1", 20) #フォント設定

                #ステージ1のボタンの描写
                stage1Button = pygame.draw.rect(self.screen, self.white,
                                                (30, 30, (self.width - 120) // 3, self.height - 60))
                stage1ButtonText = stageButtonFont.render("今はここしか選べないよ", True, self.black)
                stage1ButtonTextRect = stage1ButtonText.get_rect(center =
                                                                (30 + ((self.width - 120) // 3) // 2,
                                                                (30 + (self.height - 60) // 2)))
                self.screen.blit(stage1ButtonText, stage1ButtonTextRect)

                #ステージ2のボタンの描写
                stage2Button = pygame.draw.rect(self.screen, self.white,
                                                (60 + (self.width - 120) // 3, 30,
                                                 (self.width - 120) // 3, self.height - 60))
                stage2ButtonText = stageButtonFont.render("選べないよ", True, self.black)
                stage2ButtonTextRect = stage2ButtonText.get_rect(center =
                                                                (60 + 3 * ((self.width - 120) // 3) // 2,
                                                                (30 + (self.height - 60) // 2)))
                self.screen.blit(stage2ButtonText, stage2ButtonTextRect)

                #ステージ3のボタンの描写
                stage3Button = pygame.draw.rect(self.screen, self.white,
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
                pygame.draw.rect(self.screen, self.white, (self.stage.widthBlank, self.stage.heightBlank, (self.stage.width + 2) * self.stage.gridSize, (self.stage.height + 2) * self.stage.gridSize))

                #ステージを描画する
                stageFont = pygame.font.SysFont("ヒラキノ角コシックw1", 25) #座標を描画するフォントの設定

                for y in range(self.stage.height + 2):
                    for x in range(self.stage.width + 2):
                        state = self.stage.stage[y][x] #マスの状態を管理する変数

                        if state == 0: #マスが空白なら枠線作る
                            pygame.draw.rect(self.screen, self.stage.colors[state],
                                             (x * self.stage.gridSize + self.stage.widthBlank, y * self.stage.gridSize + self.stage.heightBlank, self.stage.gridSize, self.stage.gridSize), 1)
                        elif state == 1: #マスが壁なら壁を描写する
                            pygame.draw.rect(self.screen, self.stage.colors[state],
                                             (x * self.stage.gridSize + self.stage.widthBlank, y * self.stage.gridSize + self.stage.heightBlank, self.stage.gridSize, self.stage.gridSize))
                        elif state == 2: #マスがイベントマスならそれも描く描くしかじか
                            pygame.draw.rect(self.screen, self.stage.colors[state],
                                             (x * self.stage.gridSize + self.stage.widthBlank, y * self.stage.gridSize + self.stage.heightBlank, self.stage.gridSize, self.stage.gridSize))

                        #x軸の座標の描画．式キモめ
                        if y == 0 and x >= 1 and x <= self.stage.width:
                            xText = stageFont.render(f"{x}", True, self.white)
                            xTextRect = xText.get_rect(center = (
                                (x * self.stage.gridSize + self.stage.widthBlank) + self.stage.gridSize // 2 - 1, (y * self.stage.gridSize + self.stage.heightBlank) + self.stage.gridSize // 2))
                            self.screen.blit(xText, xTextRect)

                        #y軸の座標の描画．式キモめ2
                        if x == 0 and y >= 1 and y <= self.stage.height:
                            yText = stageFont.render(f"{chr(64+y)}", True, self.white)
                            yTextRect = yText.get_rect(center = (
                                (x * self.stage.gridSize + self.stage.widthBlank) + self.stage.gridSize // 2, (y * self.stage.gridSize + self.stage.heightBlank) + self.stage.gridSize // 2))
                            self.screen.blit(yText, yTextRect)

                #プレイヤーを描画する．これも式キモいね，ごめんね，頑張ってね
                pygame.draw.circle(self.screen, self.stage.colors["player"],
                                   (self.player.x * self.stage.gridSize + self.stage.widthBlank + self.stage.gridSize // 2, self.player.y * self.stage.gridSize + self.stage.heightBlank + self.stage.gridSize // 2), 15)

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
                pygame.draw.rect(self.screen, self.white, (0, 0, self.width, 60)) #メニューの背景を白色に
                menuFont = pygame.font.SysFont("ヒラキノ角コシックw1", 40) #メニューのフォントの設定
                menuText = menuFont.render(f"ステージ1：1F   フロア数：5   制限時間：{self.timeLimit}s", True, self.black)
                self.screen.blit(menuText, (22, 10)) #いい感じのところに配置

                #目標確認ボタン作ります
                goalButton = pygame.draw.rect(self.screen, self.black, (self.width - 90, 70, 80, 40))
                goalButtonFont = pygame.font.SysFont("ヒラキノ角コシックw1", 28) #ボタンのフォント設定
                goalButtonText = goalButtonFont.render("目標", True, self.white)
                goalButtonTextRect = goalButtonText.get_rect(center = (self.width - 90 + 80 // 2, 70 + 40 // 2))
                self.screen.blit(goalButtonText, goalButtonTextRect)

            elif self.state == "goalList": #目標確認画面の描写
                self.screen.fill(self.gray) #背景を全部灰色にする

                #目標確認リスト作ります
                goalList = pygame.draw.rect(self.screen, self.white, (50, 50, self.width - 100, self.height - 100))
                goalListFont = pygame.font.SysFont("ヒラキノ角コシックw1", 50) #フォント設定
                goalListText = goalListFont.render("ここでデータベース班の出番だ！", True, self.black)
                goalListTextRect = goalListText.get_rect(center = (self.width // 2, self.height // 2))
                self.screen.blit(goalListText, goalListTextRect)

                #戻るボタンを作ります
                backButton = pygame.draw.rect(self.screen, self.black, (10, 10, 60, 30))
                backButtonFont = pygame.font.SysFont("ヒラキノ角コシックw1", 25) #フォント設定
                backButtonText = backButtonFont.render("戻る", True, self.white)
                backButtonTextRect = backButtonText.get_rect(center = (10 + 60 // 2, 10 + 30 // 2))
                self.screen.blit(backButtonText, backButtonTextRect)

            elif self.state == "gameover": #ゲームオーバー画面の描写
                self.screen.fill(self.black) #背景を真っ黒にする
                gameoverFont = pygame.font.SysFont("ヒラキノ角コシックw1", 50) #フォント設定
                gameoverText = gameoverFont.render("げーむおーばー", True, self.red)
                gameoverTextRect = gameoverText.get_rect(center = (self.width // 2, self.height // 2))
                self.screen.blit(gameoverText, gameoverTextRect)

            pygame.display.update() #今までの変更を全部反映させる

            #イベント処理
            for event in pygame.event.get():
                if event.type == QUIT: #ウィンドウが閉じられたら終了
                    pygame.quit()
                    sys.exit()
                    
                elif event.type == KEYDOWN: #移動キー押されたら動こう
                    if self.state == "game": #ゲーム画面ならプレイヤー移動
                        self.player.move(event.key, self.stage.stage)
                        
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

            self.clock.tick(60) #60fps
                            
#メイン関数
def main():
    game = Game()
    game.run()

#実行
if __name__ == "__main__":
    main()
