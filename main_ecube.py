import cv2
import numpy as np
import perspective_transformation
import detector
import time
import os



tsf_clb = perspective_transformation.camera_tsf_clb()
# clb_mtx = tsf_clb.camera_calibration()
# print clb_mtx

# OBTAIN THE TRANSFORMATION MATRIX
tsf_matrix = tsf_clb.get_tsf_matrix()
detectors = detector.Detectors()



cap = cv2.VideoCapture(0)

pic_num = 1

img_list = []
img_name = ['img11.bmp', 'img21.bmp', 'img31.bmp', 'img32.bmp', 'img41.bmp', 'img42.bmp', 'img51.bmp', 'img52.bmp', 'img53.bmp', 'img54.bmp', 'img61.bmp', 'img62.bmp', 'img63.bmp', 'img64.bmp']

for img in img_name:
	img_path = 'pattern_img' +'/'+img
	img = cv2.imread(img_path)
	img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	img = cv2.resize(img, (120,120))
	img_list.append(img)




null_img = np.random.randint(220, size=(120, 120))
null_img = np.array(null_img ,dtype=np.uint8)

pattern_storage = np.zeros((6,5,120,120))
pattern_storage = np.array(pattern_storage ,dtype=np.uint8)


for i in range(0, 6):
	pattern_storage[i][0] = null_img
#print pattern_storage[0][0]

pattern_storage[0][1] = img_list[0]
pattern_storage[1][1] = img_list[1]

pattern_storage[2][1] = img_list[2]
pattern_storage[2][2] = img_list[3]
pattern_storage[3][1] = img_list[4]
pattern_storage[3][2] = img_list[5]

pattern_storage[4][1] = img_list[6]
pattern_storage[4][2] = img_list[7]
pattern_storage[4][3] = img_list[8]
pattern_storage[4][4] = img_list[9]

pattern_storage[5][1] = img_list[10]
pattern_storage[5][2] = img_list[11]
pattern_storage[5][3] = img_list[12]
pattern_storage[5][4] = img_list[13]

background_color = 200


while(True):
	print 'Assemly (press 1), Shape-matching (press 2), Quit (press 0)'
	game_type = input()

	if game_type == 0:
		exit()


	if game_type == 1:

		# print 'please input the pattern type'
		# pattern_type1 = input()
		# pattern_type2 = input()
		# pattern_type3 = input()

		# pattern_type = [pattern_type1, pattern_type2, pattern_type3]

		assem_test_n = 20
		assem_test_i = 0

		while (assem_test_i < assem_test_n):
			start_time = time.clock()

			while(True):
				ret, frame = cap.read()	
				# OBTAIN THE TRANSFORMED VIEW
				tsf_frame = tsf_clb.get_tsf_frame(frame, tsf_matrix)


				(w, h, c) = tsf_frame.shape
				

				show_screen = np.zeros((w, h))
				show_screen[:,:] = background_color
				show_screen = np.array(show_screen ,dtype=np.uint8)




				if assem_test_i < 10:
					# 4 blocks

					# SETUP THE SHOW SCREEN
					show_screen[100:220, 180:300] = null_img
					show_screen[100:220, 310:430] = null_img

					show_screen[230:350, 180:300] = null_img
					show_screen[230:350, 310:430] = null_img


					show_1 = show_screen[100:220, 180:300]
					show_2 = show_screen[100:220, 310:430]
					show_3 = show_screen[230:350, 180:300]
					show_4 = show_screen[230:350, 310:430]

					show_region = [show_1, show_2, show_3, show_4]

					# SPECIFY ROI 
					block_1 = tsf_frame[95:225, 175:305]
					block_2 = tsf_frame[95:225, 305:435]

					block_3 = tsf_frame[225:355, 175:305]
					block_4 = tsf_frame[225:355, 305:435]


					block_order = [block_1, block_2, block_3, block_4]


					#result = []
					index = 0
					for block in block_order:
						#print block

						white, black, bNw, result_each = detectors.single_area_checking(block)
						#result.append(result_each)
						if len(result_each) == 2:
							
							shape_result = result_each[0][0]
							angle_result = result_each[1][0]
							
							show_region[index][:,:] = pattern_storage[shape_result - 1][angle_result]

						index += 1



							


					# SET BACKGROUND COLOR
					tsf_frame[0:w, 0:180] = background_color
					tsf_frame[0:100, 180:h] = background_color
					tsf_frame[350:w, 180:430] = background_color
					tsf_frame[100:w, 430:h] = background_color

					tsf_frame[220:230, 180:430] = background_color
					tsf_frame[100:350, 300:310] = background_color


					
					# DRAW RECTANGLE ON SCREEN
					cv2.rectangle(tsf_frame,(180,100),(300,220),200,2)
					cv2.rectangle(tsf_frame,(310,100),(430,220),200,2)

					cv2.rectangle(tsf_frame,(180,230),(300,350),200,2)
					cv2.rectangle(tsf_frame,(310,230),(430,350),200,2)





				else:
					# 9 blocks

					# SETUP THE SHOW SCREEN
					show_screen[70:190, 100:220] = null_img
					show_screen[70:190, 230:350] = null_img
					show_screen[70:190, 360:480] = null_img

					show_screen[200:320, 100:220] = null_img
					show_screen[200:320, 230:350] = null_img
					show_screen[200:320, 360:480] = null_img

					show_screen[330:450, 100:220] = null_img
					show_screen[330:450, 230:350] = null_img
					show_screen[330:450, 360:480] = null_img



					show_1 = show_screen[70:190, 100:220]
					show_2 = show_screen[70:190, 230:350]
					show_3 = show_screen[70:190, 360:480]

					show_4 = show_screen[200:320, 100:220]
					show_5 = show_screen[200:320, 230:350]
					show_6 = show_screen[200:320, 360:480]


					show_7 = show_screen[330:450, 100:220]
					show_8 = show_screen[330:450, 230:350]
					show_9 = show_screen[330:450, 360:480]

					show_region = [show_1, show_2, show_3, show_4, show_5, show_6, show_7, show_8, show_9]



					# SPECIFY ROI 
					block_1 = tsf_frame[65:195, 95:225]
					block_2 = tsf_frame[65:195, 225:355]
					block_3 = tsf_frame[65:195, 355:485]

					block_4 = tsf_frame[195:325, 95:225]
					block_5 = tsf_frame[195:325, 225:355]
					block_6 = tsf_frame[195:325, 355:485]

					block_7 = tsf_frame[325:455, 95:225]
					block_8 = tsf_frame[325:455, 225:355]
					block_9 = tsf_frame[325:455, 355:485]


					block_order = [block_1, block_2, block_3, block_4, block_5, block_6, block_7, block_8, block_9]


					#result = []
					index = 0
					for block in block_order:
						#print block

						white, black, bNw, result_each = detectors.single_area_checking(block)

						if len(result_each) == 2:
							
							shape_result = result_each[0][0]
							angle_result = result_each[1][0]
							
							show_region[index][:,:] = pattern_storage[shape_result - 1][angle_result]

						index += 1
					#print result


					# SET BACKGROUND COLOR
					tsf_frame[0:w, 0:100] = background_color
					tsf_frame[0:70, 100:h] = background_color
					tsf_frame[450:w, 100:480] = background_color
					tsf_frame[70:w, 480:h] = background_color

					tsf_frame[190:200, 100:480] = background_color
					tsf_frame[320:330, 100:480] = background_color
					
					tsf_frame[70:450, 220:230] = background_color
					tsf_frame[70:450, 350:360] = background_color



					# DRAW RECTANGLE ON SCREEN
					cv2.rectangle(tsf_frame,(100,70),(220,190),200,2)
					cv2.rectangle(tsf_frame,(230,70),(350,190),200,2)
					cv2.rectangle(tsf_frame,(360,70),(480,190),200,2)

					cv2.rectangle(tsf_frame,(100,200),(220,320),200,2)
					cv2.rectangle(tsf_frame,(230,200),(350,320),200,2)
					cv2.rectangle(tsf_frame,(360,200),(480,320),200,2)

					cv2.rectangle(tsf_frame,(100,330),(220,450),200,2)
					cv2.rectangle(tsf_frame,(230,330),(350,450),200,2)
					cv2.rectangle(tsf_frame,(360,330),(480,450),200,2)



				# cv2.imshow('show_screen1', block_1)
				# cv2.imshow('show_screen2', block_2)
				# cv2.imshow('show_screen3', block_3)
				# cv2.imshow('show_screen4', block_4)
				# cv2.imshow('show_screen5', block_5)
				# cv2.imshow('show_screen6', block_6)

				# cv2.imshow('show_screen7', block_7)
				# cv2.imshow('show_screen8', block_8)
				cv2.imshow('show_screen', show_screen)
				
				cv2.imshow('tsf_frame',tsf_frame)		
				#cv2.imshow('null_img',pattern_storage[0][0])
				
				#cv2.imshow('black', black)
				#cv2.imshow('white',white)
				#cv2.imshow('bNw',bNw)
				#cv2.imshow('pattern', img11)


				end_time = time.clock()
				during_time = end_time - start_time

				switch = cv2.waitKey(1) & 0xFF

				if switch == ord('s'):# or during_time > 60:
					print 'Test',assem_test_i+1,'is checking'
					#print eva
					assem_test_i += 1
					break

				elif switch == ord('q'):
					exit()









	elif game_type == 2:

		shape_test_n = 10
		shape_test_i = 0

		while(shape_test_i < shape_test_n):
			# print 'block numbers = '
			# block_n_answer = input()
			# print 'shape numbers = '
			# shape_n_answer = input()


			start_time = time.clock()

			while(True):
				ret, frame = cap.read()	
				tsf_frame = tsf_clb.get_tsf_frame(frame, tsf_matrix)



				black, white, bNw = detectors.white_black_detector(tsf_frame)


				white,contours,hierarchy = cv2.findContours(white,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)


				#cv2.drawContours(white,contours,-1,100,3)

				block_n = detectors.block_number_detector(bNw)
				
				
				#print 'block number = ', block_n

				all_shape = []
				all_angle = []
				for contour in contours:

					perimeter = cv2.arcLength(contour,True)
					approx = cv2.approxPolyDP(contour,0.04*perimeter, True)

					shape, angle = detectors.shape_detector(approx)
					all_shape.append(shape)
					all_angle.append(angle)

				#print all_shape
				#print 'orientation:', all_angle
				eva = 'Wrong'


				if block_n == 1:
					top = detectors.top_detector(all_shape, all_angle)
					print 'top surface:',top

				elif block_n == 0:
					pass 

				else:
					#print 'block number is wrong'
					#if top == top_input:
						#eva = 'Correct'
					pass
			



				cv2.imshow('tsf_frame',tsf_frame)		
				#cv2.imshow('black', black)
				cv2.imshow('white',white)
				#cv2.imshow('bNw',bNw)


				end_time = time.clock()
				during_time = end_time - start_time

				switch = cv2.waitKey(1) & 0xFF

				if switch == ord('s'):# or during_time > 60:
					print 'Test',shape_test_i+1,'is checking'
					print eva
					shape_test_i += 1
					break

				elif switch == ord('q'):
					exit()

				elif switch == ord('w'):
					cv2.imwrite('snapshot/Assembly/A11/'+str(pic_num)+'.jpg',tsf_frame)
					pic_num += 1



	else:
		print 'Wrong Selection'

cap.release()
cv2.destroyAllWindows()

