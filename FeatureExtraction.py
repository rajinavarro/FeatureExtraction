import cv2
import numpy as np

ChainCode = []
SignalLenght = []
counter = 0
dim = (300,300)

def verifyNeighborhood(image, point, connectivity):
  global counter
  if connectivity == 4:
    print(point)
    if image[point[0]-1, point[1]] == 255:
      image[point[0]-1, point[1]] = 0
      print("0")
      return (point[0]-1, point[1])

    elif (image[point[0], point[1]+1] == 255):
      image[point[0], point[1]+1] = 0
      print('1')
      return (point[0], point[1]+1)
      
    elif (image[point[0] + 1, point[1]] == 255):
      image[point[0] + 1, point[1]] = 0
      print('2')
      return (point[0] + 1, point[1])

    elif (image[point[0], point[1]-1] == 255):
      image[point[0], point[1]-1] = 0
      print('3')
      return (point[0], point[1]-1)

    else:
      print('none')

  else:
    return point

def normalizeImage(v):
  v = (v - v.min()) / (v.max() - v.min())
  result = (v*255).astype(np.uint8)
  return result

image = cv2.imread('1_5.jpg')
image = cv2.resize(image, dim, interpolation= cv2.INTER_AREA)

imageBin = 255 - image[:, :, 0]

newIm = np.zeros(np.shape(imageBin))
kernel = np.ones((3,3), np.uint8)
newIm = normalizeImage((imageBin>100)*1)

imCopy = np.copy(newIm)
imPlot = np.zeros(np.shape(image))
imPlot[:,:,0] = imPlot[:, :, 1] = imPlot[:, :, 2] = imCopy

newIm = cv2.dilate(newIm, kernel, iterations=1) - newIm
newIm = cv2.resize(newIm, dim, interpolation= cv2.INTER_AREA)

cv2.imshow('image', newIm)
cv2.waitKey(0)
max_xy = np.where(newIm == 255)

#print(max_xy[0][0], max_xy[1][0])

newImRGB = np.zeros(np.shape(image))
newImRGB[:, :, 0] = newImRGB[:, :, 1] = newImRGB[:, :, 2] = newIm

cv2.circle(newImRGB, (max_xy[1][0], max_xy[0][0]), int(3), (0,0,255), 2)
startPoint = (max_xy[0][0], max_xy[1][0])
point = verifyNeighborhood(newIm, startPoint, 4)

while(point != startPoint):
  cv2.circle(imPlot, (point[1], point[0]), int(7), (0, 0, 255), 1)
  cv2.imshow('Image', imPlot)
  cv2.waitKey(0)
  cv2.circle(imPlot, (point[1], point[0]), int(6), (0, 255, 255), 1)
  point = verifyNeighborhood(image, point, 4)

print(ChainCode)