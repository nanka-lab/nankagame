"ここでお役立ちツールを作成します"
import os

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
