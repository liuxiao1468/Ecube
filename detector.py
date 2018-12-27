import cv2
import numpy as np
import math
from sklearn.cluster import MeanShift, estimate_bandwidth

class Detectors():


	# DETECT WHITE PART OF THE TOP SURFACE AND BLACK PART OF THE ENTIRE BLOCK
	def white_black_detector(self,frame):
		# BLACK DETECTION
		# define the color range 
		lower_black = np.array([-1,-1,-1])
		upper_black = np.array([100,100,100])


		mask1 = cv2.inRange(frame,lower_black,upper_black)
		output1 = cv2.bitwise_and(frame,frame,mask=mask1)

		# INCREASE THE CONTRAST OF THE RGB FRAME
		img_yuv = cv2.cvtColor(output1,cv2.COLOR_BGR2YUV)
		img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
		output2 = cv2.cvtColor(img_yuv,cv2.COLOR_YUV2BGR)

		
		# PRE-PROCESSING THE FRAME
		gray = cv2.cvtColor(output2,cv2.COLOR_BGR2GRAY)
		blur = cv2.blur(gray,(10,10))
		clahe = cv2.createCLAHE(clipLimit=1.8, tileGridSize=(3,3))
		cl = clahe.apply(blur)


		_,Black = cv2.threshold(blur,60,255,cv2.THRESH_BINARY)


		# WHITE DETETCION
		gray1 = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		clahe = cv2.createCLAHE(clipLimit=1.8, tileGridSize=(3,3))
		cl1 = clahe.apply(gray1)
		blur1 = cv2.blur(cl1,(6,6))

		_,White = cv2.threshold(blur1,225,255,cv2.THRESH_BINARY)

		# USE OR GATE TO COMBINE DETECTED BLACK AND WHITE AREA
		res = cv2.bitwise_or(Black,White)

		return Black, White, res
			





	# DETERMINE THE APEARRED BLOCK NUMBER
	# USED ONLY IN main_ecube.py
	def block_number_detector(self, BW_frame):

		(w, h) = BW_frame.shape
		# COUNT HOW MANY WHITE PIXEL IN THE AREA(WHITE IS THE ORIGINAL WHITE PLUS BLACK)
		detected_obj = np.sum(BW_frame)/255.
		# COUNT THE OCCRACY PERCENTAGE OF THE AREA
		detected_ratio = detected_obj/(w*h)
		block_n = "To be determined"
		#print detected_ratio

		if detected_ratio <= 0.03:
			block_n = 0

		elif 0.03 < detected_ratio <= 0.07:
			block_n = 1

		# elif 0.07 < detected_ratio <= 0.11:
		# 	block_n = 2

		# elif 0.11 < detected_ratio <= 0.142:
		# 	block_n = 3

		elif 0.13 < detected_ratio <= 0.20:
			block_n = 4

		# elif 0.20 < detected_ratio <= 0.25:
		# 	block_n = 5

		# elif 0.25 < detected_ratio <= 0.29:
		# 	block_n = 6

		# elif 0.29 < detected_ratio <= 0.33:
		# 	block_n = 7

		# elif 0.33 < detected_ratio <= 0.37:
		# 	block_n = 8

		elif 0.30 < detected_ratio <= 0.40:
			block_n = 9

		return block_n







	# DETECT THE SHAPE AND ANGLE OF THE ORIGINAL WHITE
	def shape_detector(self,approx):
		(x,y,w,h) = (0,0,0,0)
		shape = 'unidentified'
		angle = 0

		# 3 POINTS DETECTED MEANS TRIANGLE
		if len(approx) == 3:
			
			# CALCULATE THE RATIO OF THE SHORTEST LENGTH AND THE LARGEST LENGTH
			length, smallest_index, ratio = self.length_ratio(approx)
			

			# GET THE POINT CORRESPONDING TO THE SHORTEST LENGTH (THE POINT HAS NO CONNECTION TO THE SHORTEST LENGTH)
			if smallest_index == 0:
				c_point_index = len(approx)-1

			else:
				c_point_index = smallest_index - 1
				

			if ratio < 0.65:
				shape = 'right triangle'
				# GET THE ORITATION OF THE TRIANGLE 
				angle = self.triangle_orientation(c_point_index, approx, length, shape)

			else:
				shape = 'isosceles triangle'
				# GET THE ORITATION OF THE TRIANGLE 
				angle = self.triangle_orientation(c_point_index, approx, length, shape)
							
			
		# 4 POINTS DETECTED MEANS SQUARE OR RECTANGLE
		elif len(approx) == 4:

			# CALCULATE THE RATIO OF THE SHORTEST LENGTH AND THE LARGEST LENGTH
			_,_,ratio = self.length_ratio(approx)
			#print ratio
			if ratio < 0.5:
				shape = 'rectangle'
				# SORT THE FOUR CORNERS INTO A CERTAIN ORDER; 1: LEFT TOP CORNER  2: RIGHT TOP CORNER  3: LEFT BOTTOM CORNER  4: RIGHT BOTTOM CORNER 
				sorted_points = self.rectangle_sort(approx)

				# COMPUTE THE Y AXIS DIFFERENCE BETWEEN 1: LEFT TOP CORNER AND 3: LEFT BOTTOM CORNER
				vertical_diff = sorted_points[0][0] - sorted_points[2][0]		
				vertical_length = math.sqrt(np.square(vertical_diff[0]) + np.square(vertical_diff[1]))
				#print vertical_length

				if 19 < vertical_length < 34:
					angle = 1

				if 97 < vertical_length < 106:
					angle = 2

				#print vertical_length 

			else:
				shape = 'square'
				angle = 1


		else:
			print 'blackground is not clear'
			#pass
     
		return shape, angle








	def takeFirst(self,elem):
		return elem[0][0]

	def takeSecond(self,elem):
		return elem[0][1]
  
	# SORT THE FOUR CORNERS INTO A CERTAIN ORDER; 1: LEFT TOP CORNER  2: RIGHT TOP CORNER  3: LEFT BOTTOM CORNER  4: RIGHT BOTTOM CORNER   
	def rectangle_sort(self,data):
	  data1 = sorted(data , key=self.takeSecond)

	  T1 = [data1[0],data1[1]]
	  T2 = [data1[2],data1[3]]

	  T1 = sorted(T1, key=self.takeFirst)
	  T2 = sorted(T2, key=self.takeFirst)
	  data2 = [T1[0],T1[1],T2[0],T2[1]]
	  return data2







	# CALCULATE THE RATIO OF THE SHORTEST LENGTH AND THE LARGEST LENGTH
	def length_ratio(self,approx):
		length = np.zeros(len(approx))

		# COMPUTE EACH LENGTH 
		for i in range(0,len(approx)-1):
			length[i] = math.sqrt(np.square(approx[i][0][0] - approx[i+1][0][0]) + np.square(approx[i][0][1] - approx[i+1][0][1]))
		length[len(approx)-1] = math.sqrt(np.square(approx[len(approx)-1][0][0] - approx[0][0][0]) + np.square(approx[len(approx)-1][0][1] - approx[0][0][1]))

		# GET THE INDEX OF THE SHORTEST LENGTH AND THE LARGEST LENGTH
		smallest_index = length.argmin()
		largest_index = length.argmax()

		# CALCULATE THE RATIO
		ratio = length[smallest_index]/length[largest_index]

		return length, smallest_index, ratio
	      





	# GET THE ORITATION OF THE TRIANGLE 
	def triangle_orientation(self, c_point_index, approx, length, shape):

		angle = 0
		pointer = [0,1,2]
		pointer.remove(c_point_index)

		# COMPUTE THE Y AXIS DIFFERENCE BETWEEN THE POINT CORRESPONDING TO THE SHORTEST LENGTH (THE POINT HAS NO CONNECTION TO THE SHORTEST LENGTH) AND THE OTHER TWO POINTS
		diff_y1 = approx[c_point_index][0][1] - approx[pointer[0]][0][1]
		diff_y2 = approx[c_point_index][0][1] - approx[pointer[1]][0][1]

		# diff_length = np.zeros(len(length))
		# for i in range(0,len(length)-1):
		# 	diff_length[i] = length[i] - length[i+1]
		# diff_length[len(length)-1] = length[len(length)-1] - length[0]

		
		#print diff_y1
		#print diff_y2
		if -110 < diff_y1 < -80 and -110 < diff_y2 < -80:
			if shape == 'isosceles triangle':
				angle = 1
			else:
				angle = 3
			
	
		elif 80 < diff_y1 < 110 and 80 < diff_y2 < 110 :
			if shape == 'isosceles triangle':
				angle = 3
			else:
				angle = 1

			
		else:
			# COMPUTE THE X AXIS DIFFERENCE BETWEEN THE POINT CORRESPONDING TO THE SHORTEST LENGTH (THE POINT HAS NO CONNECTION TO THE SHORTEST LENGTH) AND THE OTHER TWO POINTS
			diff_x1 = approx[c_point_index][0][0] - approx[pointer[0]][0][0]
			diff_x2 = approx[c_point_index][0][0] - approx[pointer[1]][0][0]
			
			if -120 < diff_x1 < -90 and -120 < diff_x2 < -90:
				if shape == 'isosceles triangle':
					angle = 4
				else:
					angle = 2
			if 90 < diff_x1 < 120 and 90 < diff_x2 < 120:
				if shape == 'isosceles triangle':
					angle = 2
				else:
					angle = 4
		
		#if np.all(-7<all(diff_length)<7):
			#angle = 3

		return angle







	# DETERMINE TYPE OF THE BLOCK TOP SURFACE BASED ON THE DETECTED WHITE PATTERN TYPE AND ORIENTATION
	def top_detector(self, shape_type, orientation):
		shape_n = len(shape_type)
		ori_n = len(orientation)
		top = []

		# THERE IS ONE BLOCK DETECTED
		# NO PATTERN MEANS THE TOP SURFACE IS WHOLE BLACK
		# USE NUMBER TO REPRESENT THE TOP TYPE
		if shape_n == 0:
			top.append([2])

		
		elif shape_n == 1:
			if shape_type[0] == 'square':
				top.append([1])
			elif shape_type[0] == 'rectangle':
				top.append([3])
			elif shape_type[0] == 'right triangle':
				top.append([6])
			elif shape_type[0] == 'isosceles triangle':
				top.append([5])

		# TWO PATTERNS DETECTED MEANS THERE IS TWO SHAPE ON THE SINGLE TOP 
		elif shape_n == 2:
			if shape_type[0] == 'rectangle':
				top.append([4])
			elif shape_type[0] == 'right triangle':
				top.append([6])


		# NO ANGLE INFORMATION BUT ONE BLOCK IS FOUND WHICH MEANS THE TOP IS WHOLE BLACK
		if ori_n == 0:
			top.append([1])

		# ONE ANGLE INFORMATION SO USE THE DETECTED ANGLE 
		elif ori_n == 1:
			top.append([orientation[0]])

		# TWO ANGLE INFORMATION SO USE OR GATE TO GET THE FINAL DETECTED ANGLE
		elif ori_n == 2:
			top.append([orientation[0] or orientation[1]])


		return top









	# CHECK THE BLOCK SITUATION OF THE TOP SURFACE SHOWN IN THE SPECIFIED AREA 
	# USED ONLY IN main_ecube2.py
	def single_area_checking(self, area):

		black, white, bNw = self.white_black_detector(area)


		white,contours,hierarchy = cv2.findContours(white,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)


		block_n = self.single_area_block_number_detector(bNw)
		#print block_n

		all_shape = []
		all_angle = []
		top = []
		

		for contour in contours:

			perimeter = cv2.arcLength(contour,True)
			# DETERMINE THE CORNERS OF THE CONTOUR
			approx = cv2.approxPolyDP(contour,0.04*perimeter, True)

			shape, angle = self.shape_detector(approx)

			all_shape.append(shape)
			all_angle.append(angle)

		
		if block_n == 1:
			# DETERMINE TYPE OF THE BLOCK TOP SURFACE BASED ON THE DETECTED WHITE PATTERN TYPE AND ORIENTATION
			top = self.top_detector(all_shape, all_angle)

		return white, black, bNw, top







	# CHECK IF THERE IS ONE BLOCK IN THE SPECIFIED AREA; 0 BLOCK OR 1 BLOCK
	# USED ONLY IN main_ecube2.py
	def single_area_block_number_detector(self, BW_frame):

		(w, h) = BW_frame.shape
		# COUNT HOW MANY WHITE PIXEL IN THE AREA(WHITE IS THE ORIGINAL WHITE PLUS BLACK)
		detected_obj = np.sum(BW_frame)/255.
		# COUNT THE OCCRACY PERCENTAGE OF THE AREA
		detected_ratio = detected_obj/(w*h)


		if detected_ratio < 0.5:
			block_n = 0

		else:
			block_n = 1

		return block_n


		


