"""
Script for making white-painted papers from a PDF file

* PDFファイルを読み込んで、一部分を白塗りにするためのスクリプト
* [for Python 3]
* インストールが必要なもの (pip3経由など): PyMuPDF, PyPDF2

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
python3 fill_white.py TargetFile.pdf
"""

import sys
import re
import fitz
import io
from PIL import Image, ImageDraw
import PyPDF2

# 設定用変数
rects = [[100,100,200,200], [200,200,250,250]]
zoom = 3
color = (255,255,255)

if __name__ == "__main__":
    if len(sys.argv) != 2: 
        print("Usage:")
        print("python3 fill_white.py TargetFile.pdf")
        sys.exit(1)
    filename = sys.argv[1]

    # PyMuPDFを利用して１ページごとに抽出
    outputFile = PyPDF2.PdfFileWriter()
    mat = fitz.Matrix(zoom, zoom)
    pages = fitz.open(filename)
    for pagenum in range(pages.pageCount):
        # 奇数ページだけ、などは以下のコメントを参考に適宜処理を追加する
        flag = 0
        #if (pagenum%2) != 0:
        #    flag = 1
        page = pages.loadPage(pagenum)
        rgba = page.getPixmap(matrix=mat)
        rgba = Image.frombytes("RGBA", [rgba.width, rgba.height], rgba.samples)
        # RGBA のままだと保存がうまくいかなかったので、RGBに変換
        rgb = Image.new('RGB', rgba.size, (255, 255, 255))
        rgb.paste(rgba, mask=rgba.split()[3])
        draw = ImageDraw.Draw(rgb)
        if flag == 0:
            for rect in rects:
                draw.rectangle((rect[0]*zoom, rect[1]*zoom, rect[2]*zoom, rect[3]*zoom), fill=color)
        # PIL形式をPDF形式に変換。ページごとにバッファに積み上げていく。
        buf = io.BytesIO()
        rgb.convert("RGB").save(buf, format="pdf")
        outputFile.addPage(PyPDF2.PdfFileReader(buf).getPage(0))

    with open('results.pdf', 'wb') as outputStream:
        outputFile.write(outputStream)
