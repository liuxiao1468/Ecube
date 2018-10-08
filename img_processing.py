import cv2, sys
import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib.cm as cm
#from random import *
#
img1 = cv2.imread('cube7.JPG') #cube5 is specitial with highlight
img2 = cv2.imread('cube8.JPG')
img3 = cv2.imread('cube9.JPG')

img1_resize = cv2.resize(img1,(600,600))
img2_resize = cv2.resize(img2,(600,600))
img3_resize = cv2.resize(img3,(600,600))

gray1 = cv2.cvtColor(img1_resize,cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2_resize,cv2.COLOR_BGR2GRAY)
gray3 = cv2.cvtColor(img3_resize,cv2.COLOR_BGR2GRAY)

#equ = cv2.equalizeHist(gray1)
clahe = cv2.createCLAHE(clipLimit=1.8, tileGridSize=(3,3))
cl1 = clahe.apply(gray1)

cl2 = clahe.apply(gray2)

cl3 = clahe.apply(gray3)

blur1 = cv2.blur(gray1,(5,5))
blur2 = cv2.blur(gray2,(5,5))
blur3 = cv2.blur(gray3,(5,5))

ret1,mask1 = cv2.threshold(blur1,220,255,cv2.THRESH_BINARY_INV)
ret2,mask2 = cv2.threshold(blur2,220,255,cv2.THRESH_BINARY_INV)
ret3,mask3 = cv2.threshold(blur3,220,255,cv2.THRESH_BINARY_INV)

C_img1 = cv2.Canny(mask1,300,300)
C_img2 = cv2.Canny(mask2,300,300)
C_img3 = cv2.Canny(mask3,300,300)
#gray = np.float32(img)

# corners = cv2.goodFeaturesToTrack(mask4, 150, 0.01, 10)
# corners = np.int0(corners)

# for corner in corners:
#    x,y = corner.ravel()
#    cv2.circle(mask4,(x,y),3,100,-1)

cv2.imshow('img1',img1_resize)
cv2.imshow('contrast_img1',mask1)
#cv2.imshow('msk_img1',mask12)
#cv2.imshow('Canny_img1',C_img1)
#cv2.imshow('corner',corner)
cv2.imshow('img2',img2_resize)
cv2.imshow('contrast_img2',mask2)
#cv2.imshow('pro_img5',mask5)
#cv2.imshow('C_img2',C_img2)

cv2.imshow('img3',img3_resize)
cv2.imshow('contrast_img3',mask3)
#cv2.imshow('pro_img6',mask6)
#cv2.imshow('C_img3',C_img3)

if cv2.waitKey(0) & 0xFF == ord('q'):
	sys.exit()

cv2.release()
cv2.destroyAllWindows()
#cv2.waitKey(1)
