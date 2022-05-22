# -*- coding: utf-8 -*-
# =============================================================================>
# ##############################################################################
# ## 
# ## generator.py
# ## 
# ##############################################################################
# =============================================================================>
# imports
from PIL import Image
from html2image import Html2Image
import cv2
try:
    from . import google_images_download
except Exception as _:
    import google_images_download
import googlesearch
import numpy

import collections
from urllib import request
import io
import os
import glob
import shutil

TEMP_IMAGE_NAME = "tmp"
TEMP_IMAGE_FORMAT = "png"
TEMP_IMAGE = TEMP_IMAGE_NAME + "." + TEMP_IMAGE_FORMAT
TEMP_IMAGE_DIRECTORY = "../img/"
TEMP_IMAGE_PATH = TEMP_IMAGE_DIRECTORY + TEMP_IMAGE

SEARCH_LIMIT = 5 # 
COLOR_LIMIT = 20 # 

COLOR_THRESHOLD_COUNT = 255 # 0 -
COLOR_THRESHOLD_DISTANCE = 20 # 0 - 255

def rgb_to_code(r, g, b):
    color_code = "{:0>2X}{:0>2X}{:0>2X}".format(r, g, b)
    color_code = color_code.replace("0x", "")
    return color_code

def code_to_rgb(color_code):
    r = int(color_code[0:2], 16)
    g = int(color_code[2:4], 16)
    b = int(color_code[4:6], 16)
    return [r, g, b]

def color_distance(a, b):
    # CIEDE2000に変更するか
    return numpy.sqrt(numpy.sum(numpy.square(numpy.array(a) - numpy.array(b))))

class ColorProperty:
    """ColorProperty

    """
    def __init__(self, content_path):
        print("INFO:", "CONVERT")
        self.content = self._convert(content_path) # 画像をリスト化したもの
        print("INFO:", "COUNT")
        self.color = self._count(self.content) # 色:頻度
    
    def _convert(self, content_path):
        _img = cv2.imread(content_path)
        _img.resize((_img.shape[0] * _img.shape[1], 3))
        _img = _img.tolist()
        _img = [rgb_to_code(i[0], i[1], i[2]) for i in _img]
        return _img
    
    def _count(self, content):
        _dict = collections.Counter([i for i in content])
        _output = {}
        for i in _dict.most_common():
            if _dict[i[0]] >= COLOR_THRESHOLD_COUNT:
                _output[i[0]] = _dict[i[0]]
        return _output
    
    def emit_nearby_color(self):
        print("INFO:", "EMIT COLOR COUNT")

        _keys = [i for i in self.color.keys()]
        _output = {}

        while len([k for k in _output.keys()]) < COLOR_LIMIT:
            if len(_keys) < 1:
                break
            _key = _keys.pop(0)
            _tmp_keys = []
            _output[_key] = self.color[_key]

            while len(_keys) > 0:
                if self.color[_keys[0]] < COLOR_THRESHOLD_COUNT:
                    _keys.pop(0)
                elif color_distance(code_to_rgb(_key), code_to_rgb(_keys[0])) < COLOR_THRESHOLD_DISTANCE:
                    _output[_key] = _output[_key] + self.color[_keys.pop(0)]
                else:
                    _tmp_keys.append(_keys.pop(0))
            
            _keys = _tmp_keys
        
        return _output
            
# Web検索
class WebColorProperty(ColorProperty):
    """WebColorProperty

    """
    def __init__(self, target_word):
        super().__init__(target_word)
    
    def _convert(self, target_word):
        for idx, i in enumerate(googlesearch.search(target_word, num_results = SEARCH_LIMIT)):
            print("_____", "website:", i)
            hti = Html2Image()
            hti.screenshot(url = i, save_as = TEMP_IMAGE)
            shutil.move(TEMP_IMAGE, TEMP_IMAGE_DIRECTORY + "web/" + str(idx) + ".png")
        
        _output = []
        for i in glob.glob(TEMP_IMAGE_DIRECTORY + "web/*.png"):
            _output += super()._convert(i)
            os.remove(i)

        return _output

# 画像検索
class GoogleColorProperty(ColorProperty):
    """GoogleColorProperty

    """
    def __init__(self, target_word):
        super().__init__(target_word)
    
    def _convert(self, target_word):
        print("_____ ", end = "")
        _gid = google_images_download.googleimagesdownload()
        
        arguments = {
        "keywords"        : target_word,
        "limit"           : SEARCH_LIMIT,
        "format"          : "png",
        "output_directory": TEMP_IMAGE_DIRECTORY + "google/",
        "no_directory"    : True,
        "silent_mode"     : True,
        "timeout"         : 30
        }
        
        _gid.download(arguments)

        _output = []
        for i in glob.glob(TEMP_IMAGE_DIRECTORY + "google/*.png"):
            _output += super()._convert(i)
            os.remove(i)
        
        return _output

if __name__ == "__main__":
    pass
