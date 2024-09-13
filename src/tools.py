"ここでお役立ちツールを作成します"
import os
import numpy as np

#ディレクトリのパスを返す関数
#引数1はディレクトリ名
#返り値はディレクトリのパス or ディレクトリは存在しません
def find_dir_path(searching_dir):
    start_directory = os.getcwd() #最初のディレクトリを取得
    current_directory = start_directory #現在のディレクトリを設定

    while True:
        current_path = os.path.join(current_directory, searching_dir) #ディレクトリが存在すると仮定した時の現在のパス
        if os.path.isdir(current_path): #ディレクトリがこのファイルのディレクトリに存在しているかどうか
            return os.path.abspath(current_path) #ディレクトリのパスを返す
        parent_directory = os.path.abspath(os.path.join(current_directory, "..")) #現在のディレクトリの親ディレクトリ
        if parent_directory == current_directory: #現在のディレクトリ=親ディレクトリ　つまり現在ディレクトリに親がいない＝現在のディレクトリがルートディレクトリの時
            break #探索終了
        current_directory = parent_directory #現在ディレクトリを親ディレクトリに移動
    return "{%s}というディレクトリは存在しません。" % searching_dir

#numpyの2次元配列からある数値のインデックスの値を出力する　使用例；MAPの2次元配列にある「3」（プレイヤーのスタート位置）のインデックス（座標）を取得　ある数値はユニークじゃないとダメ
def find_np_array_index(array, number):
    answer_x, answer_y = np.where(array == number)
    return answer_x.item(), answer_y.item() #返り値は行、列の順だから注意 !!!!! →ここを逆にしてもいいかも

#array[x][y]がnumbersの中に入っていたらTrue
def is_position_equal(array, x, y, *numbers):
    if array[x][y] in numbers:
        return True
    else:
        return False
#使用例；print(is_position_equal([[1,2,3],[4,5,6]],1,1,5,9))

#秒を分と秒で表示する関数
def sec_convert_min(time):
    min = time // 60
    sec = time % 60
    return [min,sec]