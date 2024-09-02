import pygame, sys
from pygame.locals import *

#各変数の初期値設定
h = 9     #ステージの行数
w = 11     #ステージの列数
gs = 40     #1マスの長さ
h_blank = 150     #縦の空白部分
w_blank = 200     #横の空白部分
height = (h + 2) * gs + h_blank + (h_blank - 60)    #ウィンドウの高さ．式キモいけど見逃して．
width = (w + 2) * gs + w_blank * 2     #ウィンドウの長さ．同上
px = 1     #px, pyはプレイヤーの初期位置．とりあえず左上のマスにしとく
py = 1
stage = []     #ステージを管理する配列
game_state = 0     #0がタイトル画面，1がゲーム画面，2が目標リスト画面
running = True     #メインループ回すとき，この変数使うのが定番らしい．あまり気にしなくていい

#各色の定義
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
brown = (115, 66, 41)
orange = (233, 168, 38)
gray = (127, 127, 127)

#0が空白マス，1が壁，2がイベントマス, "player"がプレイヤーの色
colors = {0:black, 1:brown, 2:orange, "player":blue}

#ステージ生成
def stage_create():
    global stage
    
    #ステージの配列の作成
    stage = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
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

#プレイヤー操作
def player(key):
    global px, py
    old_x, old_y = px, py     #移動前のプレイヤーの場所を管理する変数

    #押されたキーに対する操作
    if key == K_a or key == K_LEFT:
        px -= 1
    elif key == K_d or key == K_RIGHT:
        px += 1
    elif key == K_w or key == K_UP:
        py -= 1
    elif key == K_s or key == K_DOWN:
        py += 1

    #移動先のマスに対する操作
    if stage[py][px] == 1:     #壁のとき
        px, py = old_x, old_y


#メイン関数
def main():
    global px, py, game_state
    pygame.init()     #おまじない．気にしなくていい
    pygame.display.set_caption("ishida' game")     #ウィンドウの名前を指定できます
    screen = pygame.display.set_mode((width, height))     #ウィンドウ作成
    stage_create()     #ステージを管理する配列を作成

    #メイン関数
    while running:
        if game_state == 0:     #タイトル画面の描写
            screen.fill(black)     #背景を全部黒にして
            
            #タイトル作ります
            font_t = pygame.font.SysFont("ヒラキノ角コシックw1", 74)     #タイトルを描画するフォントを設定
            text_t = font_t.render("なんかげーむ", True, white)
            text_t_rect = text_t.get_rect(center = (width // 2, height // 2 - 150))
            screen.blit(text_t, text_t_rect)
            
            #スタートボタン作ります
            button = pygame.draw.rect(screen, green, (width // 2 - 100, height // 2, 200, 50))
            font_b = pygame.font.SysFont("ヒラキノ角コシックw1", 28)     #ボタンのフォント設定
            text_b = font_b.render("げーむすたーと", True, black)
            text_b_rect = text_b.get_rect(center = (width // 2, height // 2 + 25))
            screen.blit(text_b, text_b_rect)
            
        elif game_state == 1:     #ゲーム画面の描写
            screen.fill(gray)     #背景を全部灰色にする
            #ステージ部分の背景を白にする．これも式キモいけど許して
            pygame.draw.rect(screen, white, (w_blank, h_blank, (w + 2) * gs, (h + 2) * gs))

            #ステージを描画する
            font_s = pygame.font.SysFont("ヒラキノ角コシックw1", 25)     #座標を描画するフォントの設定
            
            for y in range(h + 2):
                for x in range(w + 2):
                    state = stage[y][x]     #マスの状態を管理する変数

                    if state == 0:     #マスが空白なら枠線作る
                        pygame.draw.rect(screen, colors[state],
                                         (x * gs + w_blank, y * gs + h_blank, gs, gs), 1)
                    elif state == 1:     #マスが壁なら壁を描写する
                        pygame.draw.rect(screen, colors[state],
                                         (x * gs + w_blank, y * gs + h_blank, gs, gs))
                    elif state == 2:     #マスがイベントマスならそれも描く描くしかじか
                        pygame.draw.rect(screen, colors[state],
                                         (x * gs + w_blank, y * gs + h_blank, gs, gs))

                    #x軸の座標の描画．式キモめ
                    if y == 0 and x >= 1 and x <= w:
                        text_s = font_s.render(f"{x}", True, white)
                        text_s_rect = text_s.get_rect(center = (
                            (x * gs + w_blank) + gs // 2 - 1, (y * gs + h_blank) + gs // 2))
                        screen.blit(text_s, text_s_rect)

                    #y軸の座標の描画．式キモめ2
                    if x == 0 and y >= 1 and y <= h:
                        text_s = font_s.render(f"{chr(64+y)}", True, white)
                        text_s_rect = text_s.get_rect(center = (
                            (x * gs + w_blank) + gs // 2, (y * gs + h_blank) + gs // 2))
                        screen.blit(text_s, text_s_rect)

            #プレイヤーを描画する．これも式キモいね，ごめんね，頑張ってね
            pygame.draw.circle(screen, colors["player"],
                               (px * gs + w_blank + gs // 2, py * gs + h_blank + gs // 2), 15)

            #メニューの描画
            pygame.draw.rect(screen, white, (0, 0, width, 60))     #メニューの背景を白色に
            font_m = pygame.font.SysFont("ヒラキノ角コシックw1", 40)     #メニューのフォントの設定
            text_m = font_m.render("ステージ1：1F   フロア数：5   制限時間：126s", True, black)
            screen.blit(text_m, (22, 10))     #いい感じのところに配置

        pygame.display.update()     #今までの変更を全部反映させる

        #イベント処理
        for event in pygame.event.get():
            if event.type == QUIT:     #ウィンドウが閉じられたら終了
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:     #移動キー押されたら動こう
                if game_state == 1:     #ゲーム画面ならプレイヤー移動
                    player(event.key)
            elif event.type == MOUSEBUTTONDOWN:
                if game_state == 0:     #タイトル画面なら反応
                    if button.collidepoint(event.pos):     #ボタンがクリックされたら
                        game_state = 1     #ゲーム画面に移行
        
#実行
if __name__ == "__main__":
    main()
