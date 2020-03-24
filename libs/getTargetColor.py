
from tqdm import tqdm
import collections

def calcAverage(x, y, px, target):
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
  return (R_ave, G_ave, B_ave)

def calcFrequent(x, y, px, target):
  R = []
  G = []
  B = []
  for i in range(y, y + px):
    for j in range(x, x + px):
      R.append(target.getpixel((x, y))[0])
      G.append(target.getpixel((x, y))[1])
      B.append(target.getpixel((x, y))[2])
  return(collections.Counter(R).most_common()[0][0], collections.Counter(G).most_common()[0][0], collections.Counter(B).most_common()[0][0])

def calcCenter(x, y, px, target):
  R = []
  G = []
  B = []
  for i in range(y, y + px):
    for j in range(x, x + px):
      R.append(target.getpixel((x, y))[0])
      G.append(target.getpixel((x, y))[1])
      B.append(target.getpixel((x, y))[2])
  R.sort()
  G.sort()
  B.sort()
  return (R[int(len(R)/2)], G[int(len(R)/2)], B[int(len(R)/2)])

def calcTargetColor(x, y, px, target, method):
  if method == 'frequent':
    return calcFrequent(x, y, px, target)
  elif method == 'center':
    return calcCenter(x, y, px, target)
  else:
    return calcAverage(x, y, px, target)