from PIL import Image
from pymongo import MongoClient
import glob
import shutil
import datetime
import collections

def analyzeColor(image):
  # 平均の計算
  R_ave = 0
  G_ave = 0
  B_ave = 0
  # 中央値 最頻値の計算
  R = []
  G = []
  B = []
  for y in range(image.size[1]):
    for x in range(image.size[0]):
      # 平均の計算
      R_ave += image.getpixel((x, y))[0]
      G_ave += image.getpixel((x, y))[1]
      B_ave += image.getpixel((x, y))[2]
      # 中央値 最頻値の計算
      R.append(image.getpixel((x, y))[0])
      G.append(image.getpixel((x, y))[1])
      B.append(image.getpixel((x, y))[2])
  # 平均の計算
  px = image.size[0] * image.size[1]
  client = MongoClient('mongo', 27017)
  db = client['mosaic']
  collection = db['average']
  t = datetime.datetime.now()
  filename = str(datetime.datetime.timestamp(t)) + '.jpg'
  collection.insert_one({"R": int(R_ave / px), "G": int(G_ave / px), "B": int(B_ave / px), "filename": filename})

  # 中央値の計算
  R.sort()
  G.sort()
  B.sort()
  # connect mongodb and insert data
  collection = db['center']
  collection.insert_one({"R": R[int(len(R)/2)], "G": G[int(len(G)/2)], "B": B[int(len(B)/2)], "filename": filename})

  # 最頻値の計算
  r = collections.Counter(R)
  g = collections.Counter(G)
  b = collections.Counter(B)
  # insert data
  collection = db['frequent']
  collection.insert_one({"R": r.most_common()[0][0], "G": g.most_common()[0][0], "B": b.most_common()[0][0], "filename": filename})

  return filename


def analyze():
  source_dir = './../source_images/new/*'
  files = glob.glob(source_dir)
  for filename in files:
    print(filename)
    image = Image.open(filename)
    # calc color average and insert data into average collection 
    result = analyzeColor(image)   # this function returns renamed filename
    # analyzeCenterAndFrequentValueColor(image, result)
    # rename and mv target file
    shutil.move(filename, './../source_images/source/' + result)


def main():
  if glob.glob('./../source_images/new/*'):
    analyze()
  else:
    print('no new image')
  # source_dir = './../source_images/new/*'
  # files = glob.glob(source_dir)
  # for i in files:
  #   print(i)
  #   analyze(i)
  # image = Image.open(source_dir + 'image.jpg')
  # result = analyzeAverageColor(image)
  # print(result)

if __name__ == '__main__':
  main()