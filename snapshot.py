import cv2, sys
import numpy as np
import os

#from random import *
#
class snapshot():
	def __init__(self):
		cap = cv2.VideoCapture(0)
		pic_num = 1
   		if not os.path.exists('snapshot'):
   			os.makedirs('snapshot')
		
		while(True):
			ret, frame = cap.read()	
			#cv2.waitKey(400)
			#print 'hi'
			cv2.imshow('frame',frame)

			a = cv2.waitKey(1) & 0xFF

			if a == ord('q'):
				break
			
			elif a == ord('s'):
				cv2.imwrite('snapshot/'+str(pic_num)+'.jpg',frame)
				pic_num += 1



		cap.release()
		cv2.destroyAllWindows()

save_image = snapshot()
