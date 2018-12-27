import cv2
import numpy as np
import imutils
import shape_detector


def detect_ecube_shape_from_webcam():
    #ecube_cascade=cv2.CascadeClassifier('cascade.xml')
    cap = cv2.VideoCapture(0)

        
    while(True):
		ret, frame = cap.read()
		gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		clahe = cv2.createCLAHE(clipLimit=1.8, tileGridSize=(3,3))
		cl = clahe.apply(gray)
		blur = cv2.blur(cl,(6,6))
		_,mask1 = cv2.threshold(blur,220,255,cv2.THRESH_BINARY)
		#_,mask1 = cv2.threshold(blur,127,250,0)
		#canny = cv2.Canny(cl,500,500)


		img,contours,hierarchy = cv2.findContours(mask1,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
		sd = shape_detector.ShapeDetector()

			#cnt = contours[0]
		cv2.drawContours(img,contours,-1,100,3)
		x=0
		y=0
		w=0
		h=0
		n_rec = 0 
		n_iso_tri = 0
		n_rgt_tri = 0
		n_sqr = 0
		line = 0
		#print len(contours)

		for c in contours:
			shape,x,y,w,h,line = sd.detection(c)
			if shape == 'rectangle':
				n_rec += 1
			elif shape == 'square':
				n_sqr += 1 
			elif shape == 'isosceles triangle':
				n_iso_tri += 1
				#cv2.circle(mask1,(line[0][0][0],line[0][0][1]),10,10)
			elif shape == 'right triangle':
				n_rgt_tri += 1
			elif shape == 'two right triangle':
				n_rgt_tri += 2
			#cv2.rectangle(mask1,(x,y),(x+w,y+h),(255,0,0),2)
		#print ('isosceles triangle:', n_iso_tri, 'right triangle:', n_rgt_tri, 'rectangle:', n_rec, 'square:', n_sqr) 
		#print ('rectangle:', n_rec, 'square:', n_sqr) 
		


		cv2.imshow('frame',mask1)
		cv2.imshow('blur',blur)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

    cap.release()
    cv2.destroyAllWindows()
	

detect_ecube_shape_from_webcam()
