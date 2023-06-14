# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 16:37:32 2022

@author: HP
"""
from PIL import Image
import cv2
import numpy as np
from matplotlib import pyplot as plt

def increaseContrast(img,alpha,beta):
    img=cv2.addWeighted(img,alpha,np.zeros(img.shape,img.dtype),0,beta)
    return img
def filteringImages(img):
    img=cv2.GaussianBlur((img),(11,11),0)
    return img
def returnRedness(img):
    yuv=cv2.cvtColor(img,cv2.COLOR_BGR2YUV)
    y,u,v=cv2.split(yuv)
    return v
def threshold(img,T=150):
	_,img=cv2.threshold(img,T,255,cv2.THRESH_BINARY)
	return img

def morphology(img,kernelSize=7):
	kernel = np.ones((kernelSize,kernelSize),np.uint8)
	opening = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
	return opening
def findContour(img):
	contours, hierarchy = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	return contours
def findBiggestContour(contours):
    c=[cv2.contourArea(i) for i in contours]
    if len(c) <=0 :
        return 0
    return contours[c.index(max(c))]
def boundaryBox(img,contours):
    
    x,y,w,h=cv2.boundingRect(contours)
    img=cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    sign=img[y:(y+h) , x:(x+w)]
    return img,sign
def preprocessingImageToClassifier(image=None,imageSize=30,mu=89.77428691773054,std=70.85156431910688):
    image = cv2.resize(image,(imageSize,imageSize) )
    plt.imshow(image)
    image = (image - mu) / std
    image = image.reshape(imageSize,imageSize,3)
    return image
def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))

# filename=r'C:\Users\HP\Desktop\05794.png'
# #filename="IMG_2038.jpg"
# testCase=cv2.imread(filename)
# testCase=cv2.cvtColor(testCase , cv2.COLOR_BGR2RGB)
# img=np.copy(testCase)
# img=filteringImages(img)
# plt.imshow(img)
# img=returnRedness(img)
# plt.imshow(img)
# img=threshold(img,T=155)
# plt.imshow(img)
# img=morphology(img,11)
# plt.imshow(img)
# contours=findContour(img)
# big=findBiggestContour(contours)
# if type(big)==int:
#     print( "trafik işareti bulunamadı")
# testCase,sign=boundaryBox(testCase,big)
# sign=cv2.cvtColor(sign,cv2.COLOR_BGR2RGB)
# plt.imshow(testCase)
# plt.imshow(sign)










