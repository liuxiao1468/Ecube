import cv2
import numpy as np
from sklearn.cluster import KMeans

def get_corners(p_frame,frame):
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
		kmeans = KMeans(n_clusters = 4).fit(points)
		four_points = kmeans.cluster_centers_
	
	return four_points

img= cv2.imread('lala.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
four_points = get_corners(gray,img)
print four_points
cv2.imshow('frame',img)
cv2.waitKey()