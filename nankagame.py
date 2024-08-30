import sys
import random
from collections import deque

class Maze:         #迷路生成(壁伸ばし法) ※"【Python】壁伸ばし法で迷路を生成する"より
    PATH = 0
    WALL = 1

    def __init__(self, width, height, seed=0):
        self.width = width
        self.height = height
        if self.width < 5 or self.height < 5:
            sys.exit()
        if self.width % 2 == 0:
            self.width += 1
        if self.height % 2 == 0:
            self.height += 1
        self.maze = [[self.PATH for x in range(self.width)] for y in range(self.height)]
        #random.seed(seed)

    def set_outer_wall(self):
        for y in range(0, self.height):
            for x in range(0, self.width):
                if x == 0 or y == 0 or x == self.width-1 or y == self.height-1:
                    self.maze[y][x] = self.WALL
        return self.maze

    def set_maze_kabenobashi(self):
        self.set_outer_wall()
        stack = deque()
        for y in range(2, self.height-1, 2):
            for x in range(2, self.width-1, 2):
                stack.append([x,y])
        while True:
            if len(stack) == 0:
                break
            random.shuffle(stack)
            point = stack.pop()
            if self.maze[point[1]][point[0]] == self.WALL:
                continue
            self.maze[point[1]][point[0]] = self.WALL
            extend_wall = []
            extend_wall.append([point[0],point[1]])
            while True:
                directions = []
                if self.maze[point[1]-1][point[0]] == self.PATH and [point[0],point[1]-2] not in extend_wall:
                    directions.append(0)
                if self.maze[point[1]][point[0]+1] == self.PATH and [point[0]+2,point[1]] not in extend_wall:
                    directions.append(1)
                if self.maze[point[1]+1][point[0]] == self.PATH and [point[0],point[1]+2] not in extend_wall:
                    directions.append(2)
                if self.maze[point[1]][point[0]-1] == self.PATH and [point[0]-2,point[1]] not in extend_wall:
                    directions.append(3)
                if len(directions) == 0:
                    break
                direction = random.choice(directions)
                if direction == 0:
                    if self.maze[point[1]-2][point[0]] == self.WALL:
                        self.maze[point[1]-1][point[0]] = self.WALL
                        break
                    else:
                        self.maze[point[1]-1][point[0]] = self.WALL
                        self.maze[point[1]-2][point[0]] = self.WALL
                        extend_wall.append([point[0],point[1]-2])
                        point = [point[0],point[1]-2]
                elif direction == 1:
                    if self.maze[point[1]][point[0]+2] == self.WALL:
                        self.maze[point[1]][point[0]+1] = self.WALL
                        break
                    else:
                        self.maze[point[1]][point[0]+1] = self.WALL
                        self.maze[point[1]][point[0]+2] = self.WALL
                        extend_wall.append([point[0]+2,point[1]])
                        point = [point[0]+2,point[1]]
                elif direction == 2:
                    if self.maze[point[1]+2][point[0]] == self.WALL:
                        self.maze[point[1]+1][point[0]] = self.WALL
                        break
                    else:
                        self.maze[point[1]+1][point[0]] = self.WALL
                        self.maze[point[1]+2][point[0]] = self.WALL
                        extend_wall.append([point[0],point[1]+2])
                        point = [point[0],point[1]+2]
                elif direction == 3:
                    if self.maze[point[1]][point[0]-2] == self.WALL:
                        self.maze[point[1]][point[0]-1] = self.WALL
                        break
                    else:
                        self.maze[point[1]][point[0]-1] = self.WALL
                        self.maze[point[1]][point[0]-2] = self.WALL
                        extend_wall.append([point[0]-2,point[1]])
                        point = [point[0]-2,point[1]]
        return self.maze

class Map(Maze):
    EVENT = 2
    
    def __init__(self, width, height, obs, evt, seed=0):
        super().__init__(width, height, seed)
        self.map = self.set_maze_kabenobashi()
        self.obs = obs
        self.evt = evt
    
    def set_map(self):
        ostack = deque()
        pstack = deque()
        for y in range(1, self.height-1,):
            for x in range(1, self.width-1,):
                if self.map[y][x] == self.WALL:
                    ostack.append([x,y])
                else:
                    pstack.append([x,y])
        while True:
            if len(ostack) <= self.obs:
                break
            random.shuffle(ostack)
            point = ostack.pop()
            self.maze[point[1]][point[0]] = self.PATH
        for _ in range(self.evt):
            random.shuffle(pstack)
            point = pstack.pop()
            self.maze[point[1]][point[0]] = self.EVENT
        return self.map

    def print_map(self):
        for col in self.map:
            for cell in col:
                if cell == self.WALL:
                    print('#', end='')
                elif cell == self.PATH:
                    print(' ', end='')
                elif cell == self.EVENT:
                    print('o', end='')
            print()






#"""
import pygame
from pygame.locals import *
import sys

#定数設定
GS = 20 * 2                     #グリッドサイズ
ROW = 2 * 5 + 1                        #行
COL = 2 * 10 + 1                        #列
HBL = 60                        #横の空白の幅(左)
HBR = 1080 - HBL - GS * COL                       #横の空白の幅(右)
VBT = 60                        #縦の空白の幅(上)
VBB = 720 - VBT - GS * ROW                       #縦の空白の幅(下)
WIDTH = HBL + GS * COL + HBR    #ウィンドウの横幅 (とりあえず1080)
HEIGHT = VBT + GS * ROW + VBB   #ウィンドウの縦幅 (とりあえず720)


#pygameのセットアップ
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #ウィンドウを作成
pygame.display.set_caption("NANKA GAME") #ウィンドウの名前をゲーム名「NANKA GAME」に設定
clock = pygame.time.Clock()

class Player:
    
    #プレイヤー位置のセットアップ
    def __init__(self, pos):
        self.pos = pos
        self.outline = "black"
        self.fill = "royal blue"
        self.keypress = False
        self.count = 0
        self.keylevel = 3
    
    #プレイヤー位置のアップデート
    def update(self, screen):
        pos = (HBL + self.pos.x * GS + GS // 2, VBT + self.pos.y * GS + GS // 2)
        rad = GS // 2
        pygame.draw.circle(screen, self.outline, pos, rad)
        pygame.draw.circle(screen, self.fill, pos, rad - 1)
        #"""
        keys = pygame.key.get_pressed()
        
        if not self.keypress and sum(keys):
            self.keypress = True
            self.count = 10
        elif self.keypress and sum(keys):
            self.count += self.keylevel
            if self.count >= 10:
                self.count = 0
                x = int(self.pos.x)
                y = int(self.pos.y)
                
                if keys[K_w] or keys[K_UP]:
                    if 0 < y and not(MAP.map[y-1][x] == MAP.WALL):
                        self.pos.y -= 1
                        #time.sleep(0.01)
                elif keys[K_a] or keys[K_LEFT]:
                    if 0 < x and not(MAP.map[y][x-1] == MAP.WALL):
                        self.pos.x -= 1
                        #time.sleep(0.01)
                elif keys[K_s] or keys[K_DOWN]:
                    if y < ROW - 1 and not(MAP.map[y+1][x] == MAP.WALL):
                        self.pos.y += 1
                        #time.sleep(0.01)
                elif keys[K_d] or keys[K_RIGHT]:
                    if x < COL - 1 and not(MAP.map[y][x+1] == MAP.WALL):
                        self.pos.x += 1
                        #time.sleep(0.01)
                #"""
        elif self.keypress:
            self.keypress = False

#変数設定
MAP = Map(COL, ROW, 50, 10)
MAP.set_map()

#ゲーム画面の状態を管理する変数を設定
STATE_TITLE = 0 #タイトル画面
STATE_MAP = 1 #マップを表示する画面
game_state = STATE_TITLE #ゲーム画面の状態をタイトル画面に設定

#ボタン描画関数
def draw_button(screen, rect, text, font, bg_color, text_color):
    pygame.draw.rect(screen, bg_color, rect)
    rendered_text = font.render(text, True, text_color)
    screen.blit(rendered_text, (rect.x + (rect.width - rendered_text.get_width()) // 2,
                                rect.y + (rect.height - rendered_text.get_height()) // 2))

#ボタン描画
start_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)


#タイトル画面の描画関数定義
def draw_title_screen(screen, start_button_rect):
    screen.fill((0, 0, 0))  # 背景を黒にする
    font = pygame.font.Font(None, 74) #日本語のフォントを導入してください（やり方わからんby 石田)
    text = font.render("NANKA GAME", True, (255, 255, 255)) 
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 3 - text.get_height() // 2))

    # ボタンを描画
    button_font = pygame.font.Font(None, 50)　#日本語のフォントを導入してください（やり方わからんby 石田)
    draw_button(screen, start_button_rect, "Game Start", button_font, (50, 200, 50), (255, 255, 255)) #文字をゲームスタートに変更してください
    
    pygame.display.flip()





#MAP.print_map()
bgcolor = "white"                           #背景色
gridlinecolor = "black"                     #マス枠色
normalgridcolor = "white"                   #通常マス色
eventgridcolor = "sky blue"                 #イベントマス色
wallcolor = "grey30"                        #壁色
player = Player(pygame.Vector2(1, 1))       #プレイヤーの位置
keylevel = 1                                #キーレベル

#ループさせる
running = True

while running:
    # イベントの取得
    for event in pygame.event.get():
        # Xボタンで終了
        if event.type == QUIT:
            running = False

        # マウスクリックイベントの検出
        if event.type == MOUSEBUTTONDOWN:
            if game_state == STATE_TITLE:
                if start_button_rect.collidepoint(event.pos):
                    game_state = STATE_MAP

        # ゲームプレイ中のキー操作を処理
        if event.type == KEYDOWN:
            if game_state == STATE_MAP:
                if event.key in [K_w, K_a, K_s, K_d, K_UP, K_LEFT, K_DOWN, K_RIGHT]:
                    pass

    # 状態に応じた描画処理
    if game_state == STATE_TITLE:
        draw_title_screen(screen, start_button_rect)
    elif game_state == STATE_MAP:
        # 背景
        screen.fill(bgcolor)
        outline = Rect(HBL - 1, VBT - 1, GS * COL + 2, GS * ROW + 2)
        pygame.draw.rect(screen, gridlinecolor, outline)
        for h in range(ROW):
            for w in range(COL):
                outline = Rect(HBL + GS * w, VBT + GS * h, GS, GS)
                fill = Rect(HBL + 1 + GS * w, VBT + 1 + GS * h, GS - 2, GS - 2)
                pygame.draw.rect(screen, gridlinecolor, outline)
                if MAP.map[h][w] == MAP.PATH:
                    pygame.draw.rect(screen, normalgridcolor, fill)
                elif MAP.map[h][w] == MAP.EVENT:
                    pygame.draw.rect(screen, eventgridcolor, fill)
                elif MAP.map[h][w] == MAP.WALL:
                    pygame.draw.rect(screen, wallcolor, fill)
        player.update(screen)  # プレイヤー位置のアップデート
        pygame.display.flip()  # ディスプレイのアップデート

    clock.tick(60)  # FPSを60に設定する

pygame.quit()


#"""
