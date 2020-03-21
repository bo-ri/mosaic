from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import sys
from libs.analyzeColor import analyze
import glob
if glob.glob('./source_images/new/*'):
  analyze()

source_dir = './source_images/source'
target_image = './target/image.jpg'
dist_image = './dist/image.jpg'

target = Image.open(target_image)
print(target)
px = 10

width, height = target.size
dist = Image.new('RGB', target.size)

for y in range(0, height, px):
  for x in range(0, width, px):
    R = 0
    G = 0
    B = 0
    for i in range(y, y + px):
      for j in range(x, x + px):
        r, g, b = target.getpixel((j, i))
        R += r
        G += g
        B += b
    R_ave = int(R / (px * px))
    G_ave = int(G / (px * px))
    B_ave = int(B / (px * px))
    tile = Image.new(mode='RGB', size=(px, px), color=(R_ave, G_ave, B_ave))
    dist.paste(tile, (x, y))

dist.save(dist_image)

