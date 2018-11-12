import cv2
import numpy as np
import shape_detector


def detect_black_from_webcam():
    #ecube_cascade=cv2.CascadeClassifier('cascade.xml')
    cap = cv2.VideoCapture(0)

        
    while(True):
		ret, frame = cap.read()
		


		#lower_black = np.array([30,25,15])
		#upper_black = np.array([100,85,70])
		lower_black = np.array([10,10,10])
		upper_black = np.array([100,85,70])

		mask1 = cv2.inRange(frame,lower_black,upper_black)
		output1 = cv2.bitwise_and(frame,frame,mask=mask1)
		#print ('B=',output1[0,0,0],'G=',output1[0,0,1],'R=',output1[0,0,2])

		img_yuv = cv2.cvtColor(output1,cv2.COLOR_BGR2YUV)
		img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
		output2 = cv2.cvtColor(img_yuv,cv2.COLOR_YUV2BGR)

		
		
		gray = cv2.cvtColor(output2,cv2.COLOR_BGR2GRAY)
		blur = cv2.blur(gray,(10,10))
		clahe = cv2.createCLAHE(clipLimit=1.8, tileGridSize=(3,3))
		cl = clahe.apply(blur)
		
		

		_,mask3 = cv2.threshold(blur,60,255,cv2.THRESH_BINARY)
		img,contours,hierarchy = cv2.findContours(mask3,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
		cv2.drawContours(img,contours,-1,100,3)

		# sd = shape_detector.ShapeDetector()

		# x=0
		# y=0
		# w=0
		# h=0
		# n_rec = 0 
		# n_sqr = 0
		# line = 0

		# for c in contours:
		# 	shape,x,y,w,h,line = sd.detection(c)
		# 	if shape == 'rectangle':
		# 		n_rec += 1
		# 	elif shape == 'square':
		# 		n_sqr += 1 
			
		#print ('square:',n_sqr,'rectangle:',n_rec)


		
		cv2.imshow('frame',frame)
		cv2.imshow('gray',gray)
		#cv2.imshow('mask3',mask3)
		cv2.imshow('contour',img)

		

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

    cap.release()
    cv2.destroyAllWindows()
	

detect_black_from_webcam()
