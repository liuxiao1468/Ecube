import cv2, sys
import numpy as np

#from random import *
#
class video_prcessing():
	def __init__(self):
		cap = cv2.VideoCapture(0)

		
		while(True):
			ret, frame = cap.read()
			gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
			clahe = cv2.createCLAHE(clipLimit=1.8, tileGridSize=(3,3))
			cl = clahe.apply(gray)
			blur = cv2.blur(cl,(6,6))
			#_,mask1 = cv2.threshold(blur,220,255,cv2.THRESH_BINARY)
			blur_inv = cv2.bitwise_not(blur)
			#blur_inv = 255-blur
			_,mask2 = cv2.threshold(blur_inv,200,255,cv2.THRESH_BINARY)
			#_,after_mask2 = cv2.threshold(mask2,200,255,cv2.THRESH_BINARY)
			#_,mask2 = cv2.threshold(mask1,127,250,0)
			#canny = cv2.Canny(mask1,300,300)


			#img,contours,hierarchy = cv2.findContours(mask1,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)


			#cnt = contours[0]
			#cv2.drawContours(img,contours,-1,100,3)
			
			#M = cv2.moments(cnt)


			#cv2.imshow('frame1',mask1)
			cv2.imshow('frame2',blur_inv)
			#cv2.imshow('frame3',mask2)
			#cv2.imshow('frame4',blur_inv)
			#cv2.imshow('frame',canny)

			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

		cap.release()
		cv2.destroyAllWindows()

test = video_prcessing()
