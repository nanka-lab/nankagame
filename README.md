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

.
├── README.md
├── __pycache__
│   └── test_stage1.cpython-311-pytest-7.4.0.pyc
├── assets
│   └── fonts
│       └── ヒラギノ角ゴシック W1.ttc
├── docs
│   └── なんかゲーム概要.pptx
├── main.py
├── requirements.txt
├── setup.sh
├── sql
│   └── kari.sql
├── src
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-311.pyc
│   │   ├── classes.cpython-311.pyc
│   │   ├── nankagame.cpython-311.pyc
│   │   ├── test_1.cpython-311-pytest-7.4.0.pyc
│   │   └── tools.cpython-311.pyc
│   ├── classes.py
│   ├── data
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-311.pyc
│   │   │   └── consts.cpython-311.pyc
│   │   ├── consts.py
│   │   └── maps
│   │       ├── __pycache__
│   │       │   └── stage1.cpython-311.pyc
│   │       └── stage1.py
│   ├── events.py
│   ├── nankagame.py
│   └── tools.py
└── test
    ├── __init__.py
    ├── __pycache__
    │   ├── __init__.cpython-311.pyc
    │   └── test_stage1.cpython-311-pytest-7.4.0.pyc
    └── test_stage1.py

14 directories, 28 files	
