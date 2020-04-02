import cv2 as cv
import numpy as np

#importing image
path = '1_5.jpg'
img = cv.imread(path)
print(img)

#funfa perfeitamente pro 1_6.png
#funfa perfeitamente pro 1_5.png
#funfa perfeitamente pro 1_1.png
#funfa perfeitamente pro 1.jpg
#funfa perfeitamente pro 1_2.jpg

def chainCode(img, numberOfDirections=4):
    #img
    #imgThresholded
    #imgDilated

    
    #Converting img to grayscale
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    #thresholding img
    _, imgThresholded = cv.threshold(img, 200, 255,cv.THRESH_BINARY)

    #maybe the input image has a white background, so we need to invert the colors
    #we are assuming that the object is smaller than the background
    white_pixels,black_pixels = np.where(imgThresholded==255),np.where(imgThresholded==0)
    if len(white_pixels[0]) > len(black_pixels[0]):
        imgThresholded = cv.bitwise_not(imgThresholded)

    #dilating the object
    element = cv.getStructuringElement(shape=cv.MORPH_RECT, ksize=(3,3))
    imgDilated = cv.dilate(imgThresholded, element)

    #subtracting to only get the edges
    imgDilated = imgDilated - imgThresholded

    #finding the first white pixel
    initialPoint = np.where(imgDilated==255)
    initialPoint = (initialPoint[0][0], initialPoint[1][0])

    #deleting variables which will not be usefull anymore
    del imgThresholded, white_pixels, black_pixels
    
    ret_vec = []
    point = initialPoint
    
    dilatedCopy = np.zeros_like(imgDilated)
    while True:
        
        #verify if the right pixel is an edge 
        if imgDilated[point[0],point[1]+1] == 255:
            ret_vec.append(0)
            point = (point[0],point[1]+1)
            imgDilated[point] = 0
            dilatedCopy[point] = 180

        #verify if the below pixel is an edge
        elif imgDilated[point[0]+1,point[1]] == 255:
            ret_vec.append(6)
            point = (point[0]+1,point[1])
            imgDilated[point] = 0
            dilatedCopy[point] = 180
        
        #verify if the left pixel is an edge
        elif imgDilated[point[0],point[1]-1] == 255:
            ret_vec.append(4)
            point = (point[0],point[1]-1)
            imgDilated[point] = 0
            dilatedCopy[point] = 180

        #verify if the above pixel is an edge
        elif imgDilated[point[0]-1,point[1]] == 255:
            ret_vec.append(2)
            point = (point[0]-1,point[1])
            imgDilated[point] = 0
            dilatedCopy[point] = 180

        #verify if the right-down pixel is an edge 
        elif imgDilated[point[0]+1,point[1]+1] == 255:
            ret_vec.append(7)
            point = (point[0]+1,point[1]+1)
            imgDilated[point] = 0
            dilatedCopy[point] = 180

        #verify if the left-down pixel is an edge 
        elif imgDilated[point[0]-1,point[1]+1] == 255:
            ret_vec.append(5)
            point = (point[0]+1,point[1]-1)
            imgDilated[point] = 0
            dilatedCopy[point] = 180

        #verify if the left-up pixel is an edge 
        elif imgDilated[point[0]-1,point[1]-1] == 255:
            ret_vec.append(3)
            point = (point[0]-1,point[1]-1)
            imgDilated[point] = 0
            dilatedCopy[point] = 180

        #verify if the right-up pixel is an edge 
        elif imgDilated[point[0]-1,point[1]+1] == 255:
            ret_vec.append(1)
            point = (point[0]-1,point[1]+1)
            imgDilated[point] = 0
            dilatedCopy[point] = 180

        cv.imshow('dilatedCopy', dilatedCopy)
        cv.waitKey(5)

        #if we reach the initialPoint then we break    
        if point==initialPoint: break
    cv.destroyAllWindows()
    
    cv.imshow('dilatedCopy', dilatedCopy)
    cv.waitKey(0)
    cv.destroyAllWindows()
    return ret_vec
        
chainCode(img)