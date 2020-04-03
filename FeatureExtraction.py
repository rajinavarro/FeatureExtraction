import cv2
import numpy as np
import time
import matplotlib.pyplot as plt

SignalLenght = []
counter = 0
dim = (300, 300)

data_path = ["1_1.png", "1_2.jpg", "1_5.jpg", "1_6.png", "1.jpg"]


def verifyNeighborhood(image, point, connectivity, chainCode):
  global counter
  if connectivity == 4:
    
    if image[point[0]-1, point[1]] == 255:
      image[point[0]-1, point[1]] = 0
      chainCode.append(0)
      return (point[0]-1, point[1])

    elif (image[point[0], point[1]+1] == 255):
      image[point[0], point[1]+1] = 0
      chainCode.append(1)
      return (point[0], point[1]+1)

    elif (image[point[0] + 1, point[1]] == 255):
      image[point[0] + 1, point[1]] = 0
      chainCode.append(2)
      return (point[0] + 1, point[1])

    elif (image[point[0], point[1]-1] == 255):
      image[point[0], point[1]-1] = 0
      chainCode.append(3)
      return (point[0], point[1]-1)

    else:
      print('none')

  else:
    return point


def normalizeImage(v):
  v = (v - v.min()) / (v.max() - v.min())
  result = (v*255).astype(np.uint8)
  return result



def chaincode(path):
  chainCode = []
  image = cv2.imread("./data/"+path)
  image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
  
  imageBin = 255 - image[:, :, 0]
  
  newIm = np.zeros(np.shape(imageBin))
  kernel = np.ones((3, 3), np.uint8)

  newIm = normalizeImage((imageBin > 100)*1)
  

  # imCopy = np.copy(newIm)
  # imPlot = np.zeros(np.shape(image))
  # imPlot[:,:,0] = imPlot[:, :, 1] = imPlot[:, :, 2] = imCopy

  newIm = cv2.dilate(newIm, kernel, iterations=1) - newIm
  # newIm = cv2.resize(newIm, dim, interpolation= cv2.INTER_AREA)

  cv2.imshow('image', newIm)
  # cv2.waitKey(0)
  max_xy = np.where(newIm == 255)

  # print(max_xy[0][0], max_xy[1][0])

  newImRGB = np.zeros(np.shape(image))
  
  newImRGB[:, :, 0] = newImRGB[:, :, 1] = newImRGB[:, :, 2] = newIm

  cv2.circle(newImRGB, (max_xy[1][0], max_xy[0][0]), int(3), (0, 0, 255), 2)
  startPoint = (max_xy[0][0], max_xy[1][0])
  point = verifyNeighborhood(newIm, startPoint, 4, chainCode)

  while(point != startPoint):
    # cv2.circle(newImRGB, (point[1], point[0]), int(2), (0, 0, 255), 1)
    # cv2.imshow('Image', newImRGB)

    # cv2.circle(newImRGB, (point[1], point[0]), int(4), (255, 0, 0), 1)
    point = verifyNeighborhood(newIm, point, 4, chainCode)
  # print(chainCode)
  return chainCode


def codigo01(path):
  return(chaincode(path))
# print(codigo01(data_path[0]))

def codigo02(data_path):
  for i in range(len(data_path)):
    print(i)
    print(data_path[i])
    plt.subplot(len(data_path), 1, i+1)
    plt.plot(codigo01(data_path[i]))

  plt.show()
# codigo02(data_path)
