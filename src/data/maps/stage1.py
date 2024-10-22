#ステージ1のデータ
from .. import consts as c
import numpy as np
from ... import tools

#ミニゲームタイトル
MINIGAME_1 = "連打ゲーム"

#イベントマップ場所
EVENT_FLOOR = "3F"
EVENT_X = 5
EVENT_Y = "C"

#制限時間[s]
TIME_LIMIT = 120

#各階層の壁の色
WALL_COLOR = {"1F": c.BROWN, "2F": c.BLUE, "3F": c.GREEN, "4F": c.GRAY, "5F": c.CYAN}

#各階層の1マスの大きさ
GRID_SIZE = {"1F": 40, "2F": 40, "3F": 40, "4F": 40, "5F": 40}

#各階層のマップの行数
ROW_NUMBER = {"1F": 9, "2F": 9, "3F": 9, "4F": 9, "5F": 9}

#各階層のマップの列数
COLUMN_NUMBER = {"1F": 11, "2F": 11, "3F": 11, "4F": 11, "5F": 11}

#各階層の縦の空白部分
HEIGHT_BLANK = {"1F": 150, "2F": 150, "3F": 150, "4F": 150, "5F": 150}
#各階層の横の空白部分
WIDTH_BLANK = {"1F": 200, "2F": 200, "3F": 200, "4F": 200, "5F": 200}

#フロアの数
FLOOR_NUMBER = 5

#各階層のマップ
#1F rxc=11x13
MAP_1F = np.array([ [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 3, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1],
                    [1, 0, 0, 1, 0, 0, 0, 0, 1, 4, 1, 0, 1],
                    [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])

#2F
MAP_2F = np.array([ [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 6, 0, 1],
                    [1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1],
                    [1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1],
                    [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
                    [1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1],
                    [1, 5, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1],
                    [1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])

MAP_3F = np.array([ [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 10, 1, 0, 0, 0, 0, 0, 0, 0, 8, 1],
                    [1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1],
                    [1, 0, 0, 1, 0, 2, 0, 0, 0, 1, 0, 0, 1],
                    [1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
                    [1, 0, 0, 1, 0, 1, 7, 1, 0, 1, 0, 0, 1],
                    [1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1],
                    [1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                    [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])

MAP_4F = np.array([ [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
                    [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
                    [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
                    [1, 0, 12, 1, 0, 0, 1, 0, 9, 0, 0, 0, 1],
                    [1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1],
                    [1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1],
                    [1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1],
                    [1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
                    [1, 11, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])

MAP_5F = np.array([ [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 13, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                    [1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1],
                    [1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1],
                    [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
                    [1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1],
                    [1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1],
                    [1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, -1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])

#ステージ
MAP = {"1F": MAP_1F, "2F": MAP_2F, "3F": MAP_3F, "4F": MAP_4F, "5F": MAP_5F}

#プレーヤーの初期位置
#前の階の階段の番号と一致するところがスタート位置（4番から上がってきたら4番からスタート、5だったら5番からスタート)
PLAYER_INIT = tools.find_np_array_index(MAP["1F"], 3)

#プレイヤーの初期のスピードレベル
PLAYER_INIT_SPEED = None



