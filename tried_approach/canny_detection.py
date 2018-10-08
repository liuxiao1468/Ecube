import cv2
import numpy as np

img=cv2.imread('cube1.JPG')
img=cv2.resize(img,(500,500))
cv2.imshow('img',img)

#alpha=3
#beta=50

#mul_img=cv2.multiply(img,np.array(alpha))
#new_img=cv2.add(mul_img,beta)

# canny edge detector, set different lower and upper thresholds for the detector.
canny300=cv2.Canny(img,300,300)
cv2.imshow('img1',canny300)
# sobel edge detector in x and y direction
sobelx=cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)
sobely=cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5)
cv2.imshow('img2',sobelx)
cv2.imshow('img3',sobely)
laplacian=cv2.Laplacian(img,cv2.CV_64F)
cv2.imshow('img4',laplacian)
#canny300=cv2.Canny(new_img,300,300)
#cv2.imshow('img2',canny300)
#print canny300
#print img
print laplacian

cv2.waitKey()
