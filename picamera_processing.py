import cv2, sys
import numpy as np
import picamera
from time import sleep

#from random import *

class video_prcessing():
	def __init__(self):
		camera = picamera.PiCamera()
                camera.start_preview()
                camera.crop = (0.25,0.25,0.5,0.5)
		
		while(True):
			ret, frame = cap.read()
			gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
			clahe = cv2.createCLAHE(clipLimit=1.8, tileGridSize=(3,3))
			cl = clahe.apply(gray)
			blur = cv2.blur(cl,(6,6))
			_,mask1 = cv2.threshold(blur,220,255,cv2.THRESH_BINARY)
			#_,mask1 = cv2.threshold(blur,127,250,0)
			#canny = cv2.Canny(mask1,300,300)


			img,contours,hierarchy = cv2.findContours(mask1,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)


			cnt = contours[0]
			cv2.drawContours(img,cnt,-1,100,3)
			
			#M = cv2.moments(cnt)
			#print M

			# corners = cv2.goodFeaturesToTrack(canny, 25, 0.05, 10)
			# corners = np.float32(corners)

			# for corner in corners:
   # 				x,y = corner.ravel()
   # 				cv2.circle(canny,(x,y),3,100,-1)

   			# mask1 = np.float32(mask1)
   			# dst = cv2.cornerHarris(mask1,blockSize=4,ksize=5,k=0.04)
   			# dst = cv2.dilate(dst,None)
   			# mask1[dst > 0.01 * dst.max()] = 50

			cv2.imshow('frame',img)
			#cv2.imshow('frame',canny)

			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

		cap.release()
		cv2.destroyAllWindows()

test = video_prcessing()
