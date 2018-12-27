import cv2
import numpy as np
from sklearn.cluster import KMeans


class camera_tsf_clb():

	def camera_calibration(self):
		checkboard_row = 9
		checkboard_column = 7
		criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
		objp = np.zeros((checkboard_row*checkboard_column,3),np.float32)
		objp[:,:2] = np.mgrid[0:checkboard_row, 0:checkboard_column].T.reshape(-1,2)

		objpoints = [] # 3d point in real world space
		imgpoints = [] # 2d points in image plane.

		img = cv2.imread('camera_calibration_img/3.jpg')
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		
		ret, corners = cv2.findChessboardCorners(gray,(checkboard_row,checkboard_column),None)
		if ret == True:
			objpoints.append(objp)
			cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)	
			imgpoints.append(corners)

			cv2.drawChessboardCorners(img,(checkboard_row, checkboard_column),corners,ret)

			cv2.imshow('img',img)
			cv2.waitKey()

		cv2.destroyAllWindows()

		ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
		img = cv2.imread('camera_calibration_img/1.jpg')
		h, w = img.shape[:2]
		newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

		# undistort
		dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
		x, y, w, h = roi
		dst = dst[y: y+h, x:x+w]
		#cv2.imwrite('calibresult.jpg',dst)
		cv2.imshow('calibresult', dst)
		cv2.imshow('original_img',img)

		cv2.waitKey()
		cv2.destroyAllWindows()
		return mtx




	# OBTAIN THE TRANSFORMATION MATRIX
	def get_tsf_matrix(self):
		cap = cv2.VideoCapture(0)
		
		while(True):
			ret, frame = cap.read()	
			gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
			clahe = cv2.createCLAHE(clipLimit=1.8, tileGridSize=(3,3))
			cl = clahe.apply(gray)
			blur = cv2.blur(cl,(6,6))
			blur = np.float32(blur)

			# GET DETECTED FOUR CORNERS OF THE PLAY AREA
			four_points = self.get_corners(blur,frame)

			if len(four_points) != 0:
				# GET TWO SETS OF POINTS: POINTS1 IS CLUSTERED FOUR CORNERS; POINTS2 IS THE CORRESPONDING TRANSFERED FOUR POINTS IN NEW VIEW 
				pts1, pts2 = self.get_pts1_pts2(four_points,frame)
				# CALCULATE THE TRANSFORMATION MATRIX BASED ON THE COMPUTED TWO SETS OF POINTS
				tsf_matrix = cv2.getPerspectiveTransform(pts1, pts2)


			cv2.imshow('frame',frame)
			#cv2.imshow('tsf_frame', tsf_frame)
			swithch = cv2.waitKey(1) & 0xFF
			if swithch == ord('q'):
				exit()

			if swithch == ord('z'):
				break

		cap.release()
		cv2.destroyAllWindows()
		return tsf_matrix




	def takeFirst(self,elem):
		return elem[0]

	def takeSecond(self,elem):
		return elem[1]
  
  	# SORT THE FOUR CORNERS INTO A CERTAIN ORDER; 1: LEFT TOP CORNER  2: RIGHT TOP CORNER  3: LEFT BOTTOM CORNER  4: RIGHT BOTTOM CORNER 
	def rectangle_sort(self,data):
	  data1 = sorted(data , key=self.takeSecond)

	  T1 = [data1[0],data1[1]]
	  T2 = [data1[2],data1[3]]

	  T1 = sorted(T1, key=self.takeFirst)
	  T2 = sorted(T2, key=self.takeFirst)
	  data2 = [T1[0],T1[1],T2[0],T2[1]]
	  return data2




	 # FOUND CORNERS OF THE PLAY AREA
	def get_corners(self,p_frame,frame):
		# GET LOTS OF DETECTED CORNER POINTS
		dst = cv2.cornerHarris(p_frame,21,15,0.1)
			#print frame.max()
			#dst = cv2.dilate(dst,None)
		frame[dst>0.2*dst.max()] = [0,0,255]
		coord = np.where(np.all(frame == (0,0,255),axis = -1))
			
		y=coord[0]
		x=coord[1]

		points = np.matrix(zip(x,y))

		if points.shape == (1,0) :
			print "Not enough corners are found"
			four_points = []

		else:
			# CLUSTER THE CORNER POINTS INTO FOUR CLASSES 
			kmeans = KMeans(n_clusters = 4).fit(points)
			four_points = kmeans.cluster_centers_
		
		return four_points




	# POINTS1 IS CLUSTERED FOUR CORNERS; POINTS2 IS THE CORRESPONDING TRANSFERED FOUR POINTS IN NEW VIEW 
	def get_pts1_pts2(self,four_points,frame):

		four_points = four_points.astype(int)
		four_points_ar = np.array(four_points)
		# SORT THE FOUR CORNERS INTO A CERTAIN ORDER; 1: LEFT TOP CORNER  2: RIGHT TOP CORNER  3: LEFT BOTTOM CORNER  4: RIGHT BOTTOM CORNER 
		four_points_list = self.rectangle_sort(four_points.tolist())


		# POINTS1 IS CLUSTERED FOUR CORNERS
		pts1 = np.float32(four_points_list)
		# POINTS2 IS THE CORRESPONDING TRANSFERED FOUR POINTS IN NEW VIEW
		pts2 = np.float32([[686,500],[0,500],[686,0],[0,0]])
		#pts2 = np.float32([[0,0],[686,0],[0,500],[686,500]])


		# DRAW THE CORNERS AND PUT TEXT 
		cv2.circle(frame, (four_points_list[0][0],four_points_list[0][1]), 6,(255,0,0),-1)
		cv2.putText(frame,'1',(four_points_list[0][0],four_points_list[0][1]+30),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2,cv2.LINE_AA)
		cv2.circle(frame, (four_points_list[1][0],four_points_list[1][1]), 6,(255,0,0),-1)
		cv2.putText(frame,'2',(four_points_list[1][0],four_points_list[1][1]+30),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2,cv2.LINE_AA)
		cv2.circle(frame, (four_points_list[2][0],four_points_list[2][1]), 6,(255,0,0),-1)
		cv2.putText(frame,'3',(four_points_list[2][0],four_points_list[2][1]+30),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2,cv2.LINE_AA)
		cv2.circle(frame, (four_points_list[3][0],four_points_list[3][1]), 6,(255,0,0),-1)
		cv2.putText(frame,'4',(four_points_list[3][0],four_points_list[3][1]+30),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2,cv2.LINE_AA)

		# CONNECT FOUR CORNERS
		cv2.line(frame,(four_points_list[0][0],four_points_list[0][1]), (four_points_list[1][0],four_points_list[1][1]),(0,255,0),1)
		cv2.line(frame,(four_points_list[1][0],four_points_list[1][1]), (four_points_list[3][0],four_points_list[3][1]),(0,255,0),1)
		cv2.line(frame,(four_points_list[2][0],four_points_list[2][1]), (four_points_list[3][0],four_points_list[3][1]),(0,255,0),1)
		cv2.line(frame,(four_points_list[0][0],four_points_list[0][1]), (four_points_list[2][0],four_points_list[2][1]),(0,255,0),1)
			
		return pts1,pts2




	# OBTAIN THE TRANSFORMED VIEW
	def get_tsf_frame(self, frame, tsf_matrix):
		tsf_frame = cv2.warpPerspective(frame, tsf_matrix, (600,500))

		return tsf_frame




#tsf_clb = perspective_transformation.camera_tsf_clb()
# clb_mtx = tsf_clb.camera_calibration()
# print clb_mtx
