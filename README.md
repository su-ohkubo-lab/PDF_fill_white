# Script for making white-painted papers from a PDF file

* PDFファイルを読み込んで、一部分を白塗りにするためのスクリプト
* [for Python 3]
* インストールが必要なもの (```pip3```経由など): ```PyMuPDF```, ```PyPDF2```

* 特徴
- 読み込んだPDFファイルの、指定された座標を白塗りにする。
- 画像として保存する（・・となっているはず）。
- zoom で出力の解像度を指定可能 (整数: 1,2,3 くらいがよい。1が粗く、3が詳細)
- color で塗りつぶす色を指定(RGB)。塗りつぶす領域のチェック用に利用。白は(255,255,255)

使い方:
1. 本スクリプト内の上部の rect に、白塗りにする座標を指定する。
[[左上X座標, 左上Y座標, 右下X座標, 右下Y座標], [左上X座標, 左上Y座標, 右下X座標, 右下Y座標], ...]
のように複数箇所指定可能。
2. 以下で白塗り。
```shell
$ python3 fill_white.py TargetFile.pdf
```
3. ```results.pdf```が作られる。