import cv2, sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from random import *
from numpy.linalg import norm

def increase_brightness(img, value):
   hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
   h, s, v = cv2.split(hsv)

   lim = 255 - value
   # v[v > lim] = 255
   # v[v <= lim] += value

   v[v <= lim] = 255
   v[v > lim] += value

   final_hsv = cv2.merge((h, s, v))
   img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
   return img

def cannyEdge(img, minT, maxT):
# minT = 250
# maxT = 255
   edge = cv2.Canny(img, minT, maxT)
# cv2.imshow("edge",edge)
   return edge

def img_preprocessing(img):
   bright_contrast=240
   edge_initial=240
   edge_increment=15
   PF = np.array([bright_contrast, edge_initial, edge_increment], dtype=np.uint8)

   img = increase_brightness(img, value=PF[0])
   cv2.imwrite('img_pre1.png',img)
   edge= cannyEdge(img, minT=PF[1:2], maxT=PF[1:2]+PF[2:3])
   # shape=edge.shape
   # print('edges',shape)

   cv2.imwrite('img_pre2.png',edge)
   # cv2.waitKey(0)
   # cv2.destroyAllWindows()
   # return edge,PF
   return img

def hog(img):
   gx = cv2.Sobel(img, cv2.CV_32F, 1, 0)
   gy = cv2.Sobel(img, cv2.CV_32F, 0, 1)
   mag, ang = cv2.cartToPolar(gx, gy)
   bin_n = 16 # Number of bins
   bin = np.int32(bin_n*ang/(2*np.pi))

   bin_cells = []
   mag_cells = []

   cellx = celly = 8

   for i in range(0,img.shape[0]/celly):
       for j in range(0,img.shape[1]/cellx):
           bin_cells.append(bin[i*celly : i*celly+celly, j*cellx : j*cellx+cellx])
           mag_cells.append(mag[i*celly : i*celly+celly, j*cellx : j*cellx+cellx])  

   hists = [np.bincount(b.ravel(), m.ravel(), bin_n) for b, m in zip(bin_cells, mag_cells)]
   hist = np.hstack(hists)

   # transform to Hellinger kernel
   eps = 1e-7
   hist /= hist.sum() + eps
   hist = np.sqrt(hist)
   hist /= norm(hist) + eps

   return hist

# cap = cv2.VideoCapture(0)

# while(1):

#     # Take each frame
#     _, frame = cap.read()
#     frame = img_preprocessing(frame)
#     gx = cv2.Sobel(frame, cv2.CV_32F, 1, 0, ksize=1)
#     gy = cv2.Sobel(frame, cv2.CV_32F, 0, 1, ksize=1)
#     mag, angle = cv2.cartToPolar(gx, gy, angleInDegrees=True)
#     cv2.imshow('mag',mag)
img = cv2.imread('cube1.JPG')

#img1 = cv2.imread('cube1.JPG')
#img = img_preprocessing(img)
#img = cv2.imread('img_pre1.png')
scale_percent = 30 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
# resize image
resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
cv2.imshow('image-resized',resized)
#img = np.float32(resized) / 255.0
img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Calculate gradient
gx = cv2.Sobel(img, cv2.CV_32F, 1, 0, ksize=1)
gy = cv2.Sobel(img, cv2.CV_32F, 0, 1, ksize=1)

mag, angle = cv2.cartToPolar(gx, gy, angleInDegrees=True)
print(mag.shape)
# hist = hog(img)
# print(hist)
# print(hist.shape)

ret,thresh = cv2.threshold(img2,127,255,0)
print(thresh.shape)
im2,contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(im2, contours, -1, (0,255,0), 3)
cnt = contours[0]
M = cv2.moments(cnt)
print( M )


cv2.imshow('mag',mag)
cv2.imwrite('img-mag.png',mag)



cv2.imshow('angle',angle)
cv2.imwrite('img-angle.png',angle)

cv2.waitKey(0)
cv2.destroyAllWindows()