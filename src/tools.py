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

#numpyの2次元配列からある数値のインデックス＋1の値を出力する　使用例；MAPの2次元配列にある「3」（プレイヤーのスタート位置）のインデックス＋1（座標）を取得
def find_np_array_index(array, number):
    answer_x, answer_y = np.where(array == number)
    return answer_x.item()+1, answer_y.item()+1
