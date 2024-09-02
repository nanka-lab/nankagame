import pygame, sys
from pygame.locals import *

class Player():
    def __init__(self):
        #各変数の初期値設定
        self.x = 1 # x, y はプレイヤーの位置。とりあえず左上のマスにしとく。
        self.y = 1

    #プレイヤー操作
    def move(self, key, stage):
        old_x, old_y = self.x, self.y     #移動前のプレイヤーの場所を管理する変数
    
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
        if stage[self.y][self.x] == 1:     #壁のとき
            self.x, self.y = old_x, old_y

class Stage():
    def __init__(self):
        #各変数の初期値設定
        self.gridSize = 40        # 1マスの長さ
        self.height = 9           # ステージの行数
        self.width = 11           # ステージの列数
        self.heightBlank = 150   # 縦の空白部分
        self.widthBlank = 200    # 横の空白部分
        self.stage = []           # ステージを管理する配列
        # 0が空白マス，1が壁，2がイベントマス, "player"がプレイヤーの色
        self.colors = {0:(0, 0, 0), 1:(115, 66, 41), 2:(233, 168, 38), "player":(0, 0, 255)} # 順番にblack、brown、orange、blue
    
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
        self.stage = Stage()    # Stageのインスタンスを作成
        self.player = Player()  # Playerのインスタンスを作成
        self.state = 0          # 0がタイトル画面，1がゲーム画面，2が目標リスト画面
        self.running = True     # メインループ回すとき，この変数使うのが定番らしい．あまり気にしなくていい

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

        pygame.init()                              #おまじない．気にしなくていい
        pygame.display.set_caption("ishida' game") #ウィンドウの名前を指定できます
        self.screen = pygame.display.set_mode((self.width, self.height)) #ウィンドウ作成
        self.stage.createStage() #ステージを管理する配列を作成
    
    def run(self):
        while self.running:
            if self.state == 0:     #タイトル画面の描写
                self.screen.fill(self.black)     #背景を全部黒にして

                #タイトル作ります
                font_t = pygame.font.SysFont("ヒラキノ角コシックw1", 74)     #タイトルを描画するフォントを設定
                text_t = font_t.render("なんかげーむ", True, self.white)
                text_t_rect = text_t.get_rect(center = (self.width // 2, self.height // 2 - 150))
                self.screen.blit(text_t, text_t_rect)

                #スタートボタン作ります
                button_s = pygame.draw.rect(self.screen, self.green, (self.width // 2 - 100, self.height // 2, 200, 50))
                font_b = pygame.font.SysFont("ヒラキノ角コシックw1", 28)     #ボタンのフォント設定
                text_b = font_b.render("げーむすたーと", True, self.black)
                text_b_rect = text_b.get_rect(center = (self.width // 2, self.height // 2 + 25))
                self.screen.blit(text_b, text_b_rect)

            elif self.state == 1:     #ゲーム画面の描写
                self.screen.fill(self.gray)     #背景を全部灰色にする
                #ステージ部分の背景を白にする．これも式キモいけど許して
                pygame.draw.rect(self.screen, self.white, (self.stage.widthBlank, self.stage.heightBlank, (self.stage.width + 2) * self.stage.gridSize, (self.stage.height + 2) * self.stage.gridSize))

                #ステージを描画する
                font_s = pygame.font.SysFont("ヒラキノ角コシックw1", 25)     #座標を描画するフォントの設定

                for y in range(self.stage.height + 2):
                    for x in range(self.stage.width + 2):
                        state = self.stage.stage[y][x]     #マスの状態を管理する変数

                        if state == 0:     #マスが空白なら枠線作る
                            pygame.draw.rect(self.screen, self.stage.colors[state],
                                             (x * self.stage.gridSize + self.stage.widthBlank, y * self.stage.gridSize + self.stage.heightBlank, self.stage.gridSize, self.stage.gridSize), 1)
                        elif state == 1:     #マスが壁なら壁を描写する
                            pygame.draw.rect(self.screen, self.stage.colors[state],
                                             (x * self.stage.gridSize + self.stage.widthBlank, y * self.stage.gridSize + self.stage.heightBlank, self.stage.gridSize, self.stage.gridSize))
                        elif state == 2:     #マスがイベントマスならそれも描く描くしかじか
                            pygame.draw.rect(self.screen, self.stage.colors[state],
                                             (x * self.stage.gridSize + self.stage.widthBlank, y * self.stage.gridSize + self.stage.heightBlank, self.stage.gridSize, self.stage.gridSize))

                        #x軸の座標の描画．式キモめ
                        if y == 0 and x >= 1 and x <= self.stage.width:
                            text_s = font_s.render(f"{x}", True, self.white)
                            text_s_rect = text_s.get_rect(center = (
                                (x * self.stage.gridSize + self.stage.widthBlank) + self.stage.gridSize // 2 - 1, (y * self.stage.gridSize + self.stage.heightBlank) + self.stage.gridSize // 2))
                            self.screen.blit(text_s, text_s_rect)

                        #y軸の座標の描画．式キモめ2
                        if x == 0 and y >= 1 and y <= self.stage.height:
                            text_s = font_s.render(f"{chr(64+y)}", True, self.white)
                            text_s_rect = text_s.get_rect(center = (
                                (x * self.stage.gridSize + self.stage.widthBlank) + self.stage.gridSize // 2, (y * self.stage.gridSize + self.stage.heightBlank) + self.stage.gridSize // 2))
                            self.screen.blit(text_s, text_s_rect)

                #プレイヤーを描画する．これも式キモいね，ごめんね，頑張ってね
                pygame.draw.circle(self.screen, self.stage.colors["player"],
                                   (self.player.x * self.stage.gridSize + self.stage.widthBlank + self.stage.gridSize // 2, self.player.y * self.stage.gridSize + self.stage.heightBlank + self.stage.gridSize // 2), 15)

                #メニューの描画
                pygame.draw.rect(self.screen, self.white, (0, 0, self.width, 60))     #メニューの背景を白色に
                font_m = pygame.font.SysFont("ヒラキノ角コシックw1", 40)     #メニューのフォントの設定
                text_m = font_m.render("ステージ1：1F   フロア数：5   制限時間：126s", True, self.black)
                self.screen.blit(text_m, (22, 10))     #いい感じのところに配置

                #目標確認ボタン作ります
                button_g = pygame.draw.rect(self.screen, self.black, (self.width - 90, 70, 80, 40))
                font_g = pygame.font.SysFont("ヒラキノ角コシックw1", 28)     #ボタンのフォント設定
                text_g = font_g.render("目標", True, self.white)
                text_g_rect = text_g.get_rect(center = (self.width - 90 + 80 // 2, 70 + 40 // 2))
                self.screen.blit(text_g, text_g_rect)

            elif self.state == 2:     #目標確認画面の描写
                self.screen.fill(self.gray)     #背景を全部灰色にする

                #目標確認リスト作ります
                list_g = pygame.draw.rect(self.screen, self.white, (50, 50, self.width - 100, self.height - 100))
                font_l = pygame.font.SysFont("ヒラキノ角コシックw1", 50)     #フォント設定
                text_l = font_l.render("ここでデータベース班の出番だ！", True, self.black)
                text_l_rect = text_l.get_rect(center = (self.width // 2, self.height // 2))
                self.screen.blit(text_l, text_l_rect)

                #戻るボタンを作ります
                button_b = pygame.draw.rect(self.screen, self.black, (10, 10, 60, 30))
                font_b = pygame.font.SysFont("ヒラキノ角コシックw1", 25)     #フォント設定
                text_b = font_b.render("戻る", True, self.white)
                text_b_rect = text_b.get_rect(center = (10 + 60 // 2, 10 + 30 // 2))
                self.screen.blit(text_b, text_b_rect)

            pygame.display.update()     #今までの変更を全部反映させる

            #イベント処理
            for event in pygame.event.get():
                if event.type == QUIT:     #ウィンドウが閉じられたら終了
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:     #移動キー押されたら動こう
                    if self.state == 1:     #ゲーム画面ならプレイヤー移動
                        self.player.move(event.key, self.stage.stage)
                elif event.type == MOUSEBUTTONDOWN:
                    if self.state == 0:     #タイトル画面なら反応
                        if button_s.collidepoint(event.pos):     #ボタンがクリックされたら
                            self.state = 1     #ゲーム画面に移行
                    elif self.state == 1:     #ゲーム画面なら反応
                        if button_g.collidepoint(event.pos):     #ボタンがクリックされたら
                            self.state = 2     #目標確認画面に移行
                    elif self.state == 2:     #目標確認画面なら反応
                        if button_b.collidepoint(event.pos):     #ボタンがクリックされたら
                            self.state = 1     #ゲーム画面に移行

#メイン関数
def main():
    game = Game()
    game.run()

#実行
if __name__ == "__main__":
    main()