from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import sys
from libs.analyzeColor import analyze
import glob
from libs.getNearColor import getNearImagePathFromDB
# from libs.getTargetColor import calcTargetColor
from libs.getTargetColor import calcAverage
import datetime
from tqdm import tqdm

if len(glob.glob('./source_images/new/*')) > 0:
  analyze()

"""
average   平均値のコレクション
center    中央値のコレクション
frequent  最頻値のコレクション
"""
method = 'average'
# method = 'center'
# method = 'frequent'

source_dir = './source_images/source'
target_image = './target/image.jpg'
dist_image = './dist/'

image_size = 10     # upscaleするサイズ
target = Image.open(target_image)
"""
  もしも画像サイズの一の位が0ではない場合に，
  10倍するとout of rangeでerror出るから
  その場合にresizeしておく
"""
top_size, left_size = target.size
origin_top, origin_left = target.size
origin_left = list(str(origin_left))
if (not origin_left[len(origin_left)-1] is 0):
  origin_left[len(origin_left)-1] = '0'
  left_size = int(''.join(origin_left))
origin_top = list(str(origin_top))
if (not origin_top[len(origin_top)-1] is 0):
  origin_top[len(origin_top)-1] = '0'
  top_size = int(''.join(origin_top))

# 対象の画像をupscaling
# target = target.resize((top_size * image_size, left_size * image_size), Image.LANCZOS)

# 平滑化するpixel数
px = 10

width, height = target.size
dist = Image.new('RGB', (target.size[0]*image_size, target.size[1]*image_size))

"""
numbaで処理するためにPIL型のimageをnumpy配列に変換しておく
"""
li = np.array(target, dtype=None).tolist()
np_array = np.array(li, dtype=None)

"""
10px * 10pxの範囲の色情報を解析する
色相が近い画像を100px * 100pxで貼り付ける 
"""
for y in tqdm(range(0, height, px)):
  for x in range(0, width, px):
    R = 0
    G = 0
    B = 0
    color = calcAverage(x, y, px, np_array)
    img = getNearImagePathFromDB(color, method)
    tile = Image.open('./source_images/source/' + img)
    """
    LANCZOS パフォーマンスは悪いがdownscalingの品質が高い
    BICUBIC LANCZOSよりはパフォーマンスがいいが，downscalingの品質は少し落ちる
    HAMMING 妥協点としては最低
    BILINER 使うことはないだろう パフォーマンスはHAMMINGと変わらないがHAMMINGの方がdownscalingの品質が高い
    BOX     NEARESTよりはdownscalingの品質は上がる
    NEAREST defaultのfilter パフォーマンスに関してのみ最高
    """
    tile = tile.resize((px * 10, px * 10), Image.LANCZOS)
    tile.thumbnail((px * 10, px * 10), Image.LANCZOS)
    dist.paste(tile, (x * image_size, y * image_size))

t = datetime.datetime.now()
name = str(datetime.datetime.timestamp(t))
dist.save(dist_image + name + '_' + method + '.jpg')

