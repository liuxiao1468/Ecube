import cv2
import numpy as np
import math

class ShapeDetector():
	def __init__(self):
		pass

	def length_ratio(self,approx):
		length = np.zeros(len(approx))
		for i in range(0,len(approx)-1):
			length[i] = math.sqrt(np.square(approx[i][0][0] - approx[i+1][0][0]) + np.square(approx[i][0][1] - approx[i+1][0][1]))
		length[len(approx)-1] = math.sqrt(np.square(approx[len(approx)-1][0][0] - approx[0][0][0]) + np.square(approx[len(approx)-1][0][1] - approx[0][0][1]))

		smallest_l = length[0]
		largest_l = length[0]

		for j in range(1,len(approx)):
			if length[j] < smallest_l:
				smallest_l = length[j]
			elif length[j] > largest_l:
				largest_l = length[j]

		ratio = smallest_l/largest_l
		#print length
		#print smallest_l, largest_l
		#print ratio
		return length, ratio


	def detection(self,c):
		x=0
		y=0
		w=0
		h=0
		shape = 'unidentified'
		perimeter = cv2.arcLength(c,True)
		approx = cv2.approxPolyDP(c,0.04*perimeter, True)




		if len(approx) == 3:
			#shape = 'triangle'
			
			#diff_l = np.zeros(3)
			(x,y,w,h) = cv2.boundingRect(approx)
			#ar = w/float(h)
			#print ('triangle',ar)
			#shape = 'isosceles triangle' if ar >= 1 and ar <= 1.4 else 'right triangle'
			length,ratio = self.length_ratio(approx)

			if ratio < 0.65:
				shape = 'right triangle'
			else:
				shape = 'isosceles triangle'


			#print ('length:',length)
			#print ('smallest:', smallest_l)
			#print ('largest', largest_l)
			#print length
			#print ratio
			#print smallest_l
			print shape

		
			

		elif len(approx) == 4:
			(x,y,w,h) = cv2.boundingRect(approx)
			_,ratio = self.length_ratio(approx)
			#print ratio
			if ratio < 0.5:
				shape = 'rectangle'
			else:
				shape = 'square'
			print shape
			#ar = w/float(h)
			#print ('juxing',ar)
			#shape = 'square' if ar >= 0.8 and ar <= 2.5 else 'rectangle'

		elif len(approx) == 5:
			(x,y,w,h) = cv2.boundingRect(approx)
			length,ratio = self.length_ratio(approx)
			shape = '5'
			print shape
			#print length
     
		return shape,x,y,w,h,approx


