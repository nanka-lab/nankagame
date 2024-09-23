import pygame as pg
import sys, datetime, os
from pygame.locals import *  
from . import tools,classes
from .data import consts as c
from .data.maps import stage1

#フォントファイルのパスを取得
root_dir = os.path.abspath(tools.find_dir_path("nankagame")) #リポジトリのパスを取得
font_path = os.path.join(root_dir, "assets", "fonts", "ヒラギノ角ゴシック W1.ttc") #フォントファイルのパスを取得

#メインウィンドウの作成
class Screen():
    def __init__(self):
        self.width = c.WINDOW_WIDTH
        self.height = c.WINDOW_HEIGHT
        self.window = pg.display.set_mode((self.width, self.height)) #ウィンドウ作成
        pg.display.set_caption(c.TITLE_NAME) #ウィンドウの名前を指定できます
    def fill(self, color):
        self.screen.fill(color)
    def blit(self, text, rect):
        self.screen.blit(text, rect)

#タイトル画面の描画
class Title():
    def __init__(self, screen):
        self.screen = screen.window
        self.width = screen.width
        self.height = screen.height
        self.render()
    def render(self):
        self.screen.fill(c.BLACK) #背景を全部黒にして

        #タイトル作ります
        title_font = pg.font.Font(font_path, 74) #タイトルを描画するフォントを設定
        title_text = title_font.render(c.TITLE_NAME, True, c.WHITE)
        title_text_rect = title_text.get_rect(center = (self.width // 2, self.height // 2 - 150))
        self.screen.blit(title_text, title_text_rect)
        self.start_button = None

        #スタートボタン作ります
        self.start_button = pg.draw.rect(self.screen, c.GREEN, (self.width // 2 - 100, self.height // 2, 200, 50))
        start_button_font = pg.font.Font(font_path, 28) #ボタンのフォント設定
        start_button_text = start_button_font.render("げーむすたーと", True, c.BLACK)
        start_button_text_rect = start_button_text.get_rect(center = (self.width // 2, self.height // 2 + 25))
        self.screen.blit(start_button_text, start_button_text_rect)

#ステージセレクト画面の描画
class StageSelect():
    def __init__(self, screen):
        self.screen = screen.window
        self.width = screen.width
        self.height = screen.height
        self.stage1_button = None
        self.stage2_button = None
        self.stage3_button = None
        self.render()
    def render(self):
        self.screen.fill(c.GRAY) #背景を全部灰色にする
        stage_button_font = pg.font.Font(font_path, 20) #フォント設定

        #ステージ1のボタンの描写
        self.stage1_button = pg.draw.rect(self.screen, c.WHITE,
                                        (30, 30, (self.width - 120) // 3, self.height - 60))
        stage1_button_text = stage_button_font.render("今はここしか選べないよ", True, c.BLACK)
        stage1_button_text_rect = stage1_button_text.get_rect(center =
                                                        (30 + ((self.width - 120) // 3) // 2,
                                                        (30 + (self.height - 60) // 2)))
        self.screen.blit(stage1_button_text, stage1_button_text_rect)

        #ステージ2のボタンの描写
        self.stage2_button = pg.draw.rect(self.screen, c.WHITE,
                                        (60 + (self.width - 120) // 3, 30,
                                            (self.width - 120) // 3, self.height - 60))
        stage2_button_text = stage_button_font.render("選べないよ", True, c.BLACK)
        stage2_button_text_rect = stage2_button_text.get_rect(center =
                                                        (60 + 3 * ((self.width - 120) // 3) // 2,
                                                        (30 + (self.height - 60) // 2)))
        self.screen.blit(stage2_button_text, stage2_button_text_rect)

        #ステージ3のボタンの描写
        self.stage3_button = pg.draw.rect(self.screen, c.WHITE,
                                        (90 + 2 * (self.width - 120) // 3, 30,
                                            (self.width - 120) // 3, self.height - 60))
        stage3_button_text = stage_button_font.render("選べないよ", True, c.BLACK)
        stage3_button_text_rect = stage3_button_text.get_rect(center =
                                                        (90 + 5 * ((self.width - 120) // 3) // 2,
                                                        (30 + (self.height - 60) // 2)))
        self.screen.blit(stage3_button_text, stage3_button_text_rect)

#ゲーム画面の描画
class GameScreen():
    def __init__(self, game):
        self.game = game
        self.screen = game.screen.window
        self.width = game.screen.width
        self.height = game.screen.height
        self.stage = game.stage
        self.player = game.player
        self.time_limit = game.time_limit
        self.goal_button = None
        self.render()
    def render(self):
        self.screen.fill(c.GRAY) #背景を全部灰色にする
        #ステージ部分の背景を白にする．これも式キモいけど許して
        pg.draw.rect(self.screen, c.WHITE, (self.stage.width_blank, self.stage.height_blank, (self.stage.column_number + 2) * self.stage.grid_size, (self.stage.row_number + 2) * self.stage.grid_size))

        #ステージを描画する
        stage_font = pg.font.Font(font_path, 25) #座標を描画するフォントの設定
        for y in range(self.stage.row_number + 2):
            for x in range(self.stage.column_number + 2):
                state = self.stage.map[y][x] #マスの状態を管理する変数

                if state == 0: #マスが空白なら枠線作る
                    pg.draw.rect(self.screen, self.stage.get_color(state),
                                        (x * self.stage.grid_size + self.stage.width_blank, y * self.stage.grid_size + self.stage.height_blank, self.stage.grid_size, self.stage.grid_size), 1)
                else : #マスが壁なら壁を描写する
                    pg.draw.rect(self.screen, self.stage.get_color(state),
                                        (x * self.stage.grid_size + self.stage.width_blank, y * self.stage.grid_size + self.stage.height_blank, self.stage.grid_size, self.stage.grid_size))
               
                #x軸の座標の描画．式キモめ
                if y == 0 and x >= 1 and x <= self.stage.column_number:
                    x_text = stage_font.render(f"{x}", True, c.WHITE)
                    x_text_rect = x_text.get_rect(center = (
                        (x * self.stage.grid_size + self.stage.width_blank) + self.stage.grid_size // 2 - 1, (y * self.stage.grid_size + self.stage.height_blank) + self.stage.grid_size // 2))
                    self.screen.blit(x_text, x_text_rect)

                #y軸の座標の描画．式キモめ2
                if x == 0 and y >= 1 and y <= self.stage.row_number:
                    y_text = stage_font.render(f"{chr(64+y)}", True, c.WHITE)
                    y_text_rect = y_text.get_rect(center = (
                        (x * self.stage.grid_size + self.stage.width_blank) + self.stage.grid_size // 2, (y * self.stage.grid_size + self.stage.height_blank) + self.stage.grid_size // 2))
                    self.screen.blit(y_text, y_text_rect)

        #プレイヤーを描画する．これも式キモいね，ごめんね，頑張ってね
        pg.draw.circle(self.screen, c.PLAYER_COLOR,
                            (self.player.x * self.stage.grid_size + self.stage.width_blank + self.stage.grid_size // 2, self.player.y * self.stage.grid_size + self.stage.height_blank + self.stage.grid_size // 2), 15)

        #メニューの描画
        pg.draw.rect(self.screen, c.WHITE, (0, 0, self.width, 60)) #メニューの背景を白色に
        menu_font = pg.font.Font(font_path, 40) #メニューのフォントの設定
        menu_text = menu_font.render(f"ステージ1：{self.game.current_floor}F   総フロア数：{self.stage.s.FLOOR_NUMBER}   制限時間：{tools.sec_convert_min(self.time_limit)[0]}m{tools.sec_convert_min(self.time_limit)[1]}s", True, c.BLACK)
        self.screen.blit(menu_text, (22, 10)) #いい感じのところに配置

        #目標確認ボタン作ります
        self.goal_button = pg.draw.rect(self.screen, c.BLACK, (self.width - 90, 70, 80, 40))
        goal_button_font = pg.font.Font(font_path, 28) #ボタンのフォント設定
        goal_button_text = goal_button_font.render("目標", True, c.WHITE)
        goal_button_text_rect = goal_button_text.get_rect(center = (self.width - 90 + 80 // 2, 70 + 40 // 2))
        self.screen.blit(goal_button_text, goal_button_text_rect)

#目標画面の描画
class MissionScreen():
    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen.window
        self.width = self.game.screen.width
        self.height = self.game.screen.height
        self.back_button = None
        self.render()
    def render(self):
        self.screen.fill(c.GRAY) #背景を全部灰色にする

        #目標確認リスト作ります
        goal_list = pg.draw.rect(self.screen, c.WHITE, (50, 50, self.width - 100, self.height - 100))
        goal_list_font = pg.font.Font(font_path, 20) #フォント設定
        goal_list_text = goal_list_font.render(
            f"{self.game.goal_flag}, floor: {stage1.EVENT_FLOOR}, x: {stage1.EVENT_X}, y: {stage1.EVENT_Y}, {stage1.MINIGAME_1}, 報酬: なし"
            , True, c.BLACK)
        goal_list_text_rect = goal_list_text.get_rect(center = (self.width // 2, self.height // 2))
        self.screen.blit(goal_list_text, goal_list_text_rect)

        #戻るボタンを作ります
        self.back_button = pg.draw.rect(self.screen, c.BLACK, (10, 10, 60, 30))
        back_button_font = pg.font.Font(font_path, 25) #フォント設定
        back_button_text = back_button_font.render("戻る", True, c.WHITE)
        back_button_text_rect = back_button_text.get_rect(center = (10 + 60 // 2, 10 + 30 // 2))
        self.screen.blit(back_button_text, back_button_text_rect)

#ゲームオーバー画面の描画
class GameOver():
    def __init__(self,screen):
        self.screen = screen.window
        self.width = screen.width
        self.height = screen.height
        self.render()
    def render(self):
        self.screen.fill(c.BLACK) #背景を真っ黒にする
        gameover_font = pg.font.Font(font_path, 50) #フォント設定
        gameover_text = gameover_font.render("げーむおーばー", True, c.GREEN)
        gameover_text_rect = gameover_text.get_rect(center = (self.width // 2, self.height // 2))
        self.screen.blit(gameover_text, gameover_text_rect)