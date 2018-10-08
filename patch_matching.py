import cv2
import numpy as np

# total target: 8
img_shapes=cv2.imread('cube3.JPG')
# convert the image into black and white.
img_shapes=cv2.resize(img_shapes,(300,300))
img_shapes_gray=cv2.cvtColor(img_shapes,cv2.COLOR_BGR2GRAY)
template=cv2.imread('patch2.jpg',0)
w,h=template.shape[::-1]

# detect the object from the template. 
result=cv2.matchTemplate(img_shapes_gray,template,cv2.TM_CCOEFF_NORMED)
# set the threshold.
threshold=0.01
# set the detection numbers
count=0

# get the coordinates of the targets in the image.
location=np.where(result>=threshold)

# draw a rectangle in the detected location.
for pt in zip(*location[::-1]):
	cv2.rectangle(img_shapes,pt,(pt[0]+w,pt[1]+h),(255,255,0),1)
	count+=1

print 'detection numbers=',count

img=cv2.imread('cube1.JPG')
img_gray=cv2.resize(img,(400,400))
img_gray=cv2.cvtColor(img_gray,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(img_gray,127,255,0)
im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

cv2.imshow('shapes',img_shapes) 
cv2.imshow('contour',im2)
cv2.waitKey()
