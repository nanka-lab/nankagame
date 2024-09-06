@testコードの実行方法

nankagame/ディレクトリにいる状態でターミナルで$pytest

@依存関係のインストール

#nankagame/

$chmod +x setup.sh
$./setup.sh

@ゲームの始め方

main.pyを実行

@操作方法

矢印キー、wasdキー
@ディレクトリの構造

nankagame/

	-assets/　#静的資源、素材

		-fonts/

	-docs/ #資料系

		-概要資料.pttx

	-sql/	#拡張子.sql

 		-kari.sql

	-src/   #ソースコード
		
                -__init__.py

		-classes.py

		-consts.py

		-events.py

		-nankagame.py

		-tools.py

		-data/

			-maps/
		
