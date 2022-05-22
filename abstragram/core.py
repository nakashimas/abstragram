# -*- coding: utf-8 -*-
# =============================================================================>
# ##############################################################################
# ## 
# ## core.py
# ## 
# ##############################################################################
# =============================================================================>
# imports
from colorpicker import *
from composition import CompositionRandomImage

from pytrends.request import TrendReq
from PIL import Image, ImageDraw
import timeout_decorator

import shutil
import os
from datetime import datetime
from pathlib import Path
import json
import glob
import asyncio

RESOURCE_DIRECTORY = Path("../docs/_resource/")

def read_json(file_path):
    try:
        with open(file_path, "r", encoding = "utf-8") as f:
            return json.load(f)
    except json.decoder.JSONDecodeError:
        with open(file_path, "r", encoding = "utf-8-sig") as f:
            return json.load(f)
    return None

def write_json(json_data, file_path):
    with open(file_path, "w", encoding = "utf-8-sig") as f:
        json.dump(json_data, f, indent = 4, ensure_ascii = False)

class Abstragram:
    def __init__(self, trends = None):
        print("INFO:", "Abstragram initialization")
        
        _dir = RESOURCE_DIRECTORY / datetime.now().strftime('%Y_%m_%d')

        if trends is None:
            # 今日のディレクトリ作成
            if os.path.exists(_dir):
                print("_____", "Todays pictures are already exists")
            
            # トレンド取得
            pytrends = TrendReq()
            self.trends = [i for i in pytrends.trending_searches(pn = 'japan')[0]]
            
            for i in range(len(self.trends)):
                print("_____", ":", "trend", self.trends[i])
                # ディレクトリ作成
                _dir_trend = _dir / (str(i) + "_" + self.trends[i])

                if not os.path.exists(_dir_trend):
                    os.makedirs(_dir_trend)

                if not os.path.exists(_dir_trend / _dir_trend / "color.json"):
                    self.generate_color_picker(self.trends[i], _dir_trend)
                    self.generate_color_text(_dir_trend)
                    self.generate_color_image(_dir_trend)
                else:
                    print("_____", "are already exists")
        else:
            self.trends = trends
            for i in range(len(self.trends)):
                print("_____", ":", "trend", self.trends[i])
                # ディレクトリ作成
                _dir_trend = _dir / (str(i) + "_" + self.trends[i])

                if not os.path.exists(_dir_trend):
                    os.makedirs(_dir_trend)

                self.generate_color_picker(self.trends[i], _dir_trend)
                self.generate_color_text(_dir_trend)
                self.generate_color_image(_dir_trend)

        print("_____","done")
        
    def generate_color_picker(self, trend, json_path):
        print("_____", "ColorPicker")
        # 色情報のjsonを作成
        if os.path.exists(json_path):
            if not os.path.exists(json_path / "color.json"):
                _json_data = {
                    "date"  : datetime.now().strftime('%Y_%m_%d'),
                    "trend" : trend,
                    "color" : [],
                    "data"  : {}
                }

                # =================================================================>
                # WEB検索
                _web = WebColorProperty(trend)
                _json_data["data"]["web"] = _web.emit_nearby_color()

                # =================================================================>
                # 画像検索
                _pic = GoogleColorProperty(trend)
                _json_data["data"]["pic"] = _pic.emit_nearby_color()

                write_json(_json_data, json_path / "color.json")

    def generate_color_text(self, json_path):
        # 順位データに変換
        print("_____", "ColorText")
        if os.path.exists(json_path / "color.json"):
            # json読み込み
            _file = read_json(json_path / "color.json")
            _data = _file["data"]
            _color = {}

            for i in _data.keys():
                _color_dict = _data[i]
                _color_sum = sum(_data[i].values())
                _color_dict = {j:_color_dict[j] / _color_sum for j in _color_dict.keys()}

                for k in _color_dict.keys():
                    if k in _color:
                        _color[k] += _color_dict[k]
                    else:
                        _color[k] = _color_dict[k]

            _color = [k for k, v in sorted(_color.items(), key = lambda item: item[1], reverse=True)]
            _file["color"] = _color
            
            write_json(_file, json_path / "color.json")
    
    def generate_color_image(self, json_path):
        print("_____", "ColorImage")
        if os.path.exists(json_path / "color.json"):
            _tmp = [i for i in glob.glob(str(json_path / "gen/*"))]
            if len(_tmp) < 1:
                # json読み込み
                _file = read_json(json_path / "color.json")
                _color = _file["color"]
                
                for j in range(10):
                    # 枠作成
                    c = CompositionRandomImage(n_line = 8)
                    edges = c.get_edges()
                    rects = c.get_rectangles()

                    # 面積順にソート

                    rects = sorted(rects, key = lambda x: (numpy.abs(x[1][0] - x[0][0]) * numpy.abs(x[1][1] - x[0][1])), reverse = True)

                    # 描画して保存
                    im = Image.new('RGB', (1024, 1024), (255, 255, 255))
                    draw = ImageDraw.Draw(im)

                    for rec, col in zip(rects, _color):
                        draw.rectangle(
                            ((rec[0][0] * 1024, rec[0][1] * 1024), (rec[1][0] * 1024, rec[1][1] * 1024)), 
                            fill = tuple(code_to_rgb(col))
                        )
                    
                    for i in edges:
                        draw.line(((i[0][0] * 1024, i[0][1] * 1024), (i[1][0] * 1024, i[1][1] * 1024)), fill = (33, 33, 33))
                    
                    if not os.path.exists(json_path / "gen"):
                        os.makedirs(json_path / "gen")
                    
                    im.save(json_path / 'gen/{}_{}.png'.format(j, str(c.seed)[2:]), quality=95)
                
                with open(json_path / "text.txt", "w", encoding = "utf-8") as f:
                    f.write(
                        "【{}】\n\ncreated by : \n\n#{}\n#{} #{} #{} #{} #{}\n#抽象 #抽象表現 #生成 #色 #色彩 #カラー #カラーレシピ\n#trend #abstract #colors #processart #processing".format(
                            _file["trend"], _file["trend"], 
                            _color[0], _color[1], _color[2], _color[3], _color[4]
                        )
                    )

if __name__ == "__main__":
    _abs = Abstragram()