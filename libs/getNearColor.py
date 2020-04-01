from pymongo import MongoClient
import math

def calcEuclidDist(X, Y):
  return math.sqrt(((X[0] - Y[0])*(X[0] - Y[0])) + ((X[1] - Y[1])*(X[1] - Y[1])) + ((X[2] - Y[2])*(X[2] - Y[2])))

def getNearImagePathFromDB(X, col='average'):
  # r, g, b = X
  r = int(X[0])
  g = int(X[1])
  b = int(X[2])
  client = MongoClient('mongo', 27017)
  db = client['mosaic']
  collection = db[col]

  loss = 10
  while True:
    data = collection.find({'$and': [{'R':{'$gte': r - loss, '$lte': r + loss}}, {'G':{'$gte': g - loss, '$lte': g + loss}}, {'B':{'$gte': b - loss, '$lte': b + loss}}]})
    if data.count() > 0:
      break
    else:
      loss += 10

  # math.sqrt((255*255) + (255*255) + (255*255)) = 441.6729559300637
  minDistance = 442
  for doc in data:
    distance = calcEuclidDist((r, g, b), (doc['R'], doc['G'], doc['B']))
    if distance < minDistance:
      minDistance = distance
      filename = doc['filename']
  # print('mindistance: ', minDistance, '\nfilename: ', filename)
  return filename

def main():
  filename = getNearImagePathFromDB((223, 140, 201))


if __name__ == '__main__':
  main()