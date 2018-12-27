import cv2
import numpy as np
import perspective_transformation
import detector
import time



tsf_clb = perspective_transformation.camera_tsf_clb()
# clb_mtx = tsf_clb.camera_calibration()
# print clb_mtx
tsf_matrix = tsf_clb.get_tsf_matrix()
detectors = detector.Detectors()



cap = cv2.VideoCapture(0)


# READ PATTERN FROM THE FILE
img_list = []
img_name = ['img11.bmp', 'img21.bmp', 'img31.bmp', 'img32.bmp', 'img41.bmp', 'img42.bmp', 'img51.bmp', 'img52.bmp', 'img53.bmp', 'img54.bmp', 'img61.bmp', 'img62.bmp', 'img63.bmp', 'img64.bmp']

for img in img_name:
	img_path = 'pattern_img' +'/'+img
	img = cv2.imread(img_path)
	img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	img = cv2.resize(img, (120,120))
	img_list.append(img)



# RANDOM IMAGE FOR NON-BLOCK SHOWING
null_img = np.random.randint(220, size=(120, 120))
null_img = np.array(null_img ,dtype=np.uint8)

# CREATE A MATRIX TO STORE ALL THE PATTERNS
pattern_storage = np.zeros((6,5,120,120))
pattern_storage = np.array(pattern_storage ,dtype=np.uint8)


# IF THE ANGLE IS 0, SHOW THE RANDOM IMAGE CREATED WHICH MEANS THERE IS NO BLOCK OR THE BLOCK INFORMATION IS UNCOMPLETED
for i in range(0, 6):
	pattern_storage[i][0] = null_img


# FOR EXTRACTING PATTERN CONVINIENTLY, STORE THE PATTERN IN THE MATRIX
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



# QUESTION FOR ASSEMLY
# 4 BLOCKS COMBINATION
question_a = []
question_a.append([pattern_storage[1][1], pattern_storage[1][1], pattern_storage[1][1], pattern_storage[1][1]])
question_a.append([pattern_storage[1][1], pattern_storage[0][1], pattern_storage[0][1], pattern_storage[1][1]])
question_a.append([pattern_storage[1][1], pattern_storage[3][1], pattern_storage[3][1], pattern_storage[1][1]])
question_a.append([pattern_storage[1][1], pattern_storage[3][1], pattern_storage[2][2], pattern_storage[1][1]])
question_a.append([pattern_storage[1][1], pattern_storage[0][1], pattern_storage[2][2], pattern_storage[3][2]])

question_a.append([pattern_storage[2][1], pattern_storage[2][1], pattern_storage[3][1], pattern_storage[3][1]])
question_a.append([pattern_storage[2][1], pattern_storage[3][2], pattern_storage[2][2], pattern_storage[3][1]])
question_a.append([pattern_storage[5][1], pattern_storage[5][1], pattern_storage[4][3], pattern_storage[4][3]])
question_a.append([pattern_storage[5][2], pattern_storage[5][3], pattern_storage[5][1], pattern_storage[5][4]])
question_a.append([pattern_storage[5][2], pattern_storage[4][3], pattern_storage[4][1], pattern_storage[5][4]])

# 9 BLOCKS COMBINATION
question_a.append([pattern_storage[1][1], pattern_storage[0][1], pattern_storage[1][1], pattern_storage[0][1], pattern_storage[1][1], pattern_storage[0][1], pattern_storage[1][1], pattern_storage[0][1], pattern_storage[1][1]])
question_a.append([pattern_storage[1][1], pattern_storage[1][1], pattern_storage[1][1], pattern_storage[2][1], pattern_storage[2][1], pattern_storage[2][1], pattern_storage[1][1], pattern_storage[1][1], pattern_storage[1][1]])
question_a.append([pattern_storage[2][1], pattern_storage[2][1], pattern_storage[2][1], pattern_storage[3][1], pattern_storage[3][1], pattern_storage[3][1], pattern_storage[2][1], pattern_storage[2][1], pattern_storage[2][1]])
question_a.append([pattern_storage[3][2], pattern_storage[3][1], pattern_storage[3][2], pattern_storage[3][1], pattern_storage[2][2], pattern_storage[3][1], pattern_storage[3][2], pattern_storage[3][1], pattern_storage[3][2]])
question_a.append([pattern_storage[3][1], pattern_storage[2][2], pattern_storage[3][1], pattern_storage[2][1], pattern_storage[2][2], pattern_storage[2][1], pattern_storage[3][1], pattern_storage[2][2], pattern_storage[3][1]])

question_a.append([pattern_storage[2][2], pattern_storage[2][1], pattern_storage[2][2], pattern_storage[3][1], pattern_storage[3][1], pattern_storage[3][1], pattern_storage[3][2], pattern_storage[2][1], pattern_storage[3][2]])
question_a.append([pattern_storage[5][1], pattern_storage[3][2], pattern_storage[5][1], pattern_storage[1][1], pattern_storage[2][1], pattern_storage[1][1], pattern_storage[5][3], pattern_storage[3][2], pattern_storage[5][3]])
question_a.append([pattern_storage[5][1], pattern_storage[5][3], pattern_storage[5][1], pattern_storage[3][2], pattern_storage[3][1], pattern_storage[3][2], pattern_storage[5][3], pattern_storage[5][1], pattern_storage[5][3]])
question_a.append([pattern_storage[5][1], pattern_storage[5][2], pattern_storage[5][3], pattern_storage[5][2], pattern_storage[5][1], pattern_storage[5][4], pattern_storage[5][3], pattern_storage[5][4], pattern_storage[5][1]])
question_a.append([pattern_storage[5][1], pattern_storage[4][2], pattern_storage[4][3], pattern_storage[4][4], pattern_storage[4][3], pattern_storage[5][2], pattern_storage[5][3], pattern_storage[4][1], pattern_storage[5][4]])


# ANSWER FOR ASSEMBLY
# 4 BLOCKS COMBINATION
answer_a = []
answer_a.append([[[2], [1]], [[2], [1]], [[2], [1]], [[2], [1]]])
answer_a.append([[[2], [1]], [[1], [1]], [[1], [1]], [[2], [1]]])
answer_a.append([[[2], [1]], [[4], [1]], [[4], [1]], [[2], [1]]])
answer_a.append([[[2], [1]], [[4], [1]], [[3], [2]], [[2], [1]]])
answer_a.append([[[2], [1]], [[1], [1]], [[3], [2]], [[4], [2]]])

answer_a.append([[[3], [1]], [[3], [1]], [[4], [1]], [[4], [1]]])
answer_a.append([[[3], [1]], [[4], [2]], [[3], [2]], [[4], [1]]])
answer_a.append([[[6], [1]], [[6], [1]], [[5], [3]], [[5], [3]]])
answer_a.append([[[6], [2]], [[6], [3]], [[6], [1]], [[6], [4]]])
answer_a.append([[[6], [2]], [[5], [3]], [[5], [1]], [[6], [4]]])

# 9 BLOCKS COMBINATION
answer_a.append([[[2], [1]], [[1], [1]], [[2], [1]], [[1], [1]], [[2], [1]], [[1], [1]], [[2], [1]], [[1], [1]],[[2], [1]]])
answer_a.append([[[2], [1]], [[2], [1]], [[2], [1]], [[3], [1]], [[3], [1]], [[3], [1]], [[2], [1]], [[2], [1]],[[2], [1]]])
answer_a.append([[[3], [1]], [[3], [1]], [[3], [1]], [[4], [1]], [[4], [1]], [[4], [1]], [[3], [1]], [[3], [1]],[[3], [1]]])
answer_a.append([[[4], [2]], [[4], [1]], [[4], [2]], [[4], [1]], [[3], [2]], [[4], [1]], [[4], [2]], [[4], [1]],[[4], [2]]])
answer_a.append([[[4], [1]], [[3], [2]], [[4], [1]], [[3], [1]], [[3], [2]], [[3], [1]], [[4], [1]], [[3], [2]],[[4], [1]]])

answer_a.append([[[3], [2]], [[3], [1]], [[3], [2]], [[4], [1]], [[4], [1]], [[4], [1]], [[4], [2]], [[3], [1]],[[4], [2]]])
answer_a.append([[[6], [1]], [[4], [2]], [[6], [1]], [[2], [1]], [[3], [1]], [[2], [1]], [[6], [3]], [[4], [2]],[[6], [3]]])
answer_a.append([[[6], [1]], [[6], [3]], [[6], [1]], [[4], [2]], [[4], [1]], [[4], [2]], [[6], [3]], [[6], [1]],[[6], [3]]])
answer_a.append([[[6], [1]], [[6], [2]], [[6], [3]], [[6], [2]], [[6], [1]], [[6], [4]], [[6], [3]], [[6], [4]],[[6], [1]]])
answer_a.append([[[6], [1]], [[5], [2]], [[5], [3]], [[5], [4]], [[5], [3]], [[6], [2]], [[6], [3]], [[5], [1]],[[6], [4]]])


# QUESTION FOR SHAPE-MATCHING
# 4 BLOCKS COMBINATION
question_s = []
question_s.append([pattern_storage[5][1], pattern_storage[5][1], pattern_storage[5][1]])
question_s.append([pattern_storage[5][4], pattern_storage[5][2], pattern_storage[5][4]])
question_s.append([pattern_storage[5][2], pattern_storage[5][3], pattern_storage[5][1]])
question_s.append([pattern_storage[3][1], pattern_storage[3][2], pattern_storage[3][2]])
question_s.append([pattern_storage[4][1], pattern_storage[5][1], pattern_storage[3][2]])

# 9 BLOCKS
question_s.append([pattern_storage[3][2],pattern_storage[2][1],pattern_storage[3][2],pattern_storage[2][2],pattern_storage[3][1],pattern_storage[2][2], pattern_storage[3][2],pattern_storage[2][1]])
question_s.append([pattern_storage[5][1],pattern_storage[5][4],pattern_storage[5][1],pattern_storage[5][2],pattern_storage[5][1],pattern_storage[5][4], pattern_storage[5][3],pattern_storage[5][2]])
question_s.append([pattern_storage[0][1],pattern_storage[3][2],pattern_storage[2][2],pattern_storage[0][1],pattern_storage[4][4],pattern_storage[5][4], pattern_storage[0][1],pattern_storage[1][1]])
question_s.append([pattern_storage[5][1],pattern_storage[5][4],pattern_storage[5][3],pattern_storage[3][2],pattern_storage[3][1],pattern_storage[3][2], pattern_storage[4][4],pattern_storage[4][1]])
question_s.append([pattern_storage[5][1],pattern_storage[4][2],pattern_storage[5][4],pattern_storage[4][3],pattern_storage[5][3],pattern_storage[4][4], pattern_storage[5][2],pattern_storage[4][1]])


# ANSWER FOR SHAP-MATCHING
# 4 BLOCKS COMBINATION
answer_s = []
answer_s.append([[[6],[1]]])
answer_s.append([[[6],[2]]])
answer_s.append([[[6],[4]]])
answer_s.append([[[4],[1]]])
answer_s.append([[[3],[2]]])
# 9 BLOCKS COMBINATION
answer_s.append([[[4],[2]]])
answer_s.append([[[6],[3]]])
answer_s.append([[[1],[1]]])
answer_s.append([[[5],[2]]])
answer_s.append([[[6],[3]]])


# SCREEN BACKGROUND COLOR
background_color = 200


#################################################################################################################################################################################
while(True):

	# SELECT GAME TYPE OR QUIT THE GAME
	print 'Assemly (press 1), Shape-matching (press 2), Quit (press 0)'
	game_type = input()


	# QUIT THE GAME
	if game_type == 0:
		exit()

	##############################################################################################################################################
	# ASSEMABLY GAME
	if game_type == 1:

		# 20 ROUNDS IN ASSEMBLY GAME
		assem_test_n = 20
		assem_test_i = 0

		# ITERATE 20 TIMES 
		while (assem_test_i < assem_test_n):

			# START TO COUNT THE TIME 
			start_time = time.clock()

			while(True):
				ret, frame = cap.read()	

				# TRANSFORM THE VIEW 
				tsf_frame = tsf_clb.get_tsf_frame(frame, tsf_matrix)

				# GET THE WIDTH AND HEIGHT OF THE SCREEN
				(w, h, _) = tsf_frame.shape
				
				# CREATE A SCREEN TO SHOW THE REAL-TIME DETERMINED BLOCK TYPE AND ANGLE  
				show_screen = np.zeros((w, h))
				show_screen[:,:] = background_color
				show_screen = np.array(show_screen ,dtype=np.uint8)


				# CREATE A SCREEN TO SHOW THE QUESTION PATTERN COMBINATIONS
				question_screen = np.zeros((w, h))
				question_screen[:,:] = background_color
				question_screen = np.array(show_screen ,dtype=np.uint8)



				# 10 ROUNDS FOR 4 BLOCK COMBINATION IN ASSEMBLY GAME
				if assem_test_i < 10:
					
					# SETUP THE BLOCK-SHOWING AREA IN THE SHOW SCREEN
					show_screen[102:222, 182:302] = null_img
					show_screen[102:222, 304:424] = null_img

					show_screen[224:344, 182:302] = null_img
					show_screen[224:344, 304:424] = null_img

					# GIVE THE AREA TO CERTAIN NAMES SO THAT WE COULD CHANGE THE INFORMATION OF THIS AREA EASILY LATER
					show_1 = show_screen[102:222, 182:302]
					show_2 = show_screen[102:222, 304:424]
					show_3 = show_screen[224:344, 182:302]
					show_4 = show_screen[224:344, 304:424]

					show_region = [show_1, show_2, show_3, show_4]



					# SETUP THE BLOCK-SHOWING AREA IN THE QUESTION SCREEN
					question_screen[105:225, 185:305] = question_a[assem_test_i][0]
					question_screen[105:225, 305:425] = question_a[assem_test_i][1]
					question_screen[225:345, 185:305] = question_a[assem_test_i][2]
					question_screen[225:345, 305:425] = question_a[assem_test_i][3]




					# SPECIFY ROI; WITLL DETERMINE THE SITUATION OF THE BLOCK IN THESE AREA 
					block_1 = tsf_frame[95:225, 175:305]
					block_2 = tsf_frame[95:225, 305:435]

					block_3 = tsf_frame[225:355, 175:305]
					block_4 = tsf_frame[225:355, 305:435]


					block_order = [block_1, block_2, block_3, block_4]


					result = []
					index = 0

					for block in block_order:

						# CHECK THE BLOCK TYPE AND ANGLE FOR EACH SPECIFIED AREA
						white, black, bNw, result_each = detectors.single_area_checking(block)
						
						# IF BLOCK TYPE AND ANGLE INFORMATION IS COMPLETED, APPEND THE RESULT
						if len(result_each) == 2:

							result.append(result_each)
							shape_result = result_each[0][0]
							angle_result = result_each[1][0]
							
							# SHOW THE DETERMINED PATTERN IN THE SPECIFIED AREA IN SHOW SCREEN
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
					# 9 blocks COMBINATION IN ASSEMBLY GAME

					# SETUP THE BLOCK-SHOWING AREA IN THE QUESTION SCREEN
					question_screen[75:195, 125:245] = question_a[assem_test_i][0]
					question_screen[75:195, 245:365] = question_a[assem_test_i][1]
					question_screen[75:195, 365:485] = question_a[assem_test_i][2]

					question_screen[195:315, 125:245] = question_a[assem_test_i][3]
					question_screen[195:315, 245:365] = question_a[assem_test_i][4]
					question_screen[195:315, 365:485] = question_a[assem_test_i][5]

					question_screen[315:435, 125:245] = question_a[assem_test_i][6]
					question_screen[315:435, 245:365] = question_a[assem_test_i][7]
					question_screen[315:435, 365:485] = question_a[assem_test_i][8]


					# SETUP THE BLOCK-SHOWING AREA IN THE SHOW SCREEN
					show_screen[72:192, 102:222] = null_img
					show_screen[72:192, 224:344] = null_img
					show_screen[72:192, 346:466] = null_img

					show_screen[194:314, 102:222] = null_img
					show_screen[194:314, 224:344] = null_img
					show_screen[194:314, 346:466] = null_img

					show_screen[316:436, 102:222] = null_img
					show_screen[316:436, 224:344] = null_img
					show_screen[316:436, 346:466] = null_img



					show_1 = show_screen[72:192, 102:222]
					show_2 = show_screen[72:192, 224:344]
					show_3 = show_screen[72:192, 346:466]

					show_4 = show_screen[194:314, 102:222]
					show_5 = show_screen[194:314, 224:344]
					show_6 = show_screen[194:314, 346:466]


					show_7 = show_screen[316:436, 102:222]
					show_8 = show_screen[316:436, 224:344] 
					show_9 = show_screen[316:436, 346:466]

					show_region = [show_1, show_2, show_3, show_4, show_5, show_6, show_7, show_8, show_9]



					# SPECIFY ROI; WITLL DETERMINE THE SITUATION OF THE BLOCK IN THESE AREA 
					block_1 = tsf_frame[65:195, 95:225]
					block_2 = tsf_frame[65:195, 225:355]
					block_3 = tsf_frame[65:195, 355:485]

					block_4 = tsf_frame[195:325, 95:225]
					block_5 = tsf_frame[195:325, 225:355]
					block_6 = tsf_frame[195:325, 355:485]

					block_7 = tsf_frame[325:455, 95:225]
					block_8 = tsf_frame[325:455, 225:355]
					block_9 = tsf_frame[325:455, 355:485]
					# block_1 = tsf_frame[72:192, 102:222]
					# block_2 = tsf_frame[72:192, 224:344]
					# block_3= tsf_frame[72:192, 346:466]

					# block_4 = tsf_frame[194:314, 102:222]
					# block_5 = tsf_frame[194:314, 224:344]
					# block_6 = tsf_frame[194:314, 346:466]


					# block_7 = tsf_frame[316:436, 102:222]
					# block_8 = tsf_frame[316:436, 224:344] 
					# block_9 = tsf_frame[316:436, 346:466]


					block_order = [block_1, block_2, block_3, block_4, block_5, block_6, block_7, block_8, block_9]


					result = []
					index = 0
					for block in block_order:

						# CHECK THE BLOCK TYPE AND ANGLE FOR EACH SPECIFIED AREA
						white, black, bNw, result_each = detectors.single_area_checking(block)

						# IF BLOCK TYPE AND ANGLE INFORMATION IS COMPLETED, APPEND THE RESULT
						if len(result_each) == 2:
							
							result.append(result_each)
							shape_result = result_each[0][0]
							angle_result = result_each[1][0]
							
							# SHOW THE DETERMINED PATTERN IN THE SPECIFIED AREA IN SHOW SCREEN
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

				cv2.imshow('question_screen', question_screen)	
				
				#cv2.imshow('black', black)
				#cv2.imshow('white',white)
				#cv2.imshow('bNw',bNw)


				# END THE TIME COUNTING; CACULATE THE TIME PEROID 
				end_time = time.clock()
				during_time = end_time - start_time

				switch = cv2.waitKey(1) & 0xFF

				
				# CHECK THE RESULT TO SEE IF IT IS CORRECT
				if switch == ord('s'):# or during_time > 60:
					print 'Assembly Test', assem_test_i+1, 'is checking'
					
					#print result, answer_a[assem_test_i]


					if result == answer_a[assem_test_i]:
						print 'correct'
						print 'time =', during_time

					else:
						print 'wrong'

					assem_test_i += 1
					break

				# QUIT THE GAME
				elif switch == ord('q'):
					exit()

				# GO BACK TO THE PREVIOUS QUESTION
				elif switch == ord('a'):
					assem_test_i -= 1




	##################################################################################################################################################
	# SHAPE-MATCHING GAME
	elif game_type == 2:

		# 10 ROUNDS IN SHAPE-MACHING GAME
		shape_test_n = 10
		shape_test_i = 0

		while(shape_test_i < shape_test_n):

			# COUNT THE START TIME
			start_time = time.clock()

			while(True):
				ret, frame = cap.read()	
				tsf_frame = tsf_clb.get_tsf_frame(frame, tsf_matrix)


				(w, h, c) = tsf_frame.shape

				# INITIALIZE THE SHOW SCREEN
				show_screen = np.zeros((w, h))
				show_screen[:,:] = background_color
				show_screen = np.array(show_screen ,dtype=np.uint8)


				# 5 ROUNDS FOR 4 BLOCK COMBINATION IN ASSEMBLY GAME
				if shape_test_i < 5:

					show_screen[225:345, 305:425] = null_img

					# SPECIFY ROI 
					show_1 = show_screen[225:345, 305:425]
					block = tsf_frame[225:345, 305:425]

					


					# SETUP THE SHOW SCREEN
					show_screen[105:225, 185:305] = question_s[shape_test_i][0]
					show_screen[105:225, 305:425] = question_s[shape_test_i][1]
					show_screen[225:345, 185:305] = question_s[shape_test_i][2]



					
					tsf_frame[105:225, 185:305] = cv2. cvtColor(question_s[shape_test_i][0], cv2.COLOR_GRAY2RGB)
					tsf_frame[105:225, 305:425] = cv2. cvtColor(question_s[shape_test_i][1], cv2.COLOR_GRAY2RGB)

					tsf_frame[225:345, 185:305] = cv2. cvtColor(question_s[shape_test_i][2], cv2.COLOR_GRAY2RGB)
		



					result = []
					white, black, bNw, result_each = detectors.single_area_checking(block)
					
					if len(result_each) == 2:

						result.append(result_each)
						shape_result = result_each[0][0]
						angle_result = result_each[1][0]
						#print shape_result, angle_result
						
						show_1[:,:] = pattern_storage[shape_result - 1][angle_result]



							


					# SET BACKGROUND COLOR
					tsf_frame[0:w, 0:185] = background_color
					tsf_frame[0:105, 185:h] = background_color
					tsf_frame[345:w, 185:425] = background_color
					tsf_frame[105:w, 425:h] = background_color

					# tsf_frame[225:225, 180:430] = background_color
					# tsf_frame[100:350, 300:310] = background_color


					
					# DRAW RECTANGLE ON SCREEN
					# cv2.rectangle(tsf_frame,(180,100),(300,220),200,2)
					# cv2.rectangle(tsf_frame,(310,100),(430,220),200,2)

					# cv2.rectangle(tsf_frame,(180,230),(300,350),200,2)
					# cv2.rectangle(tsf_frame,(310,230),(430,350),200,2)



				else:
					# 9 blocks
					show_screen[315:435, 365:485] = null_img

					show_1 = show_screen[315:435, 365:485]

					block = tsf_frame[315:435, 365:485]



					# SETUP THE SHOW SCREEN
					show_screen[75:195, 125:245] = question_s[shape_test_i][0]
					show_screen[75:195, 245:365] = question_s[shape_test_i][1]
					show_screen[75:195, 365:485] = question_s[shape_test_i][2]

					show_screen[195:315, 125:245] = question_s[shape_test_i][3]
					show_screen[195:315, 245:365] = question_s[shape_test_i][4]
					show_screen[195:315, 365:485] = question_s[shape_test_i][5]

					show_screen[315:435, 125:245] = question_s[shape_test_i][6]
					show_screen[315:435, 245:365] = question_s[shape_test_i][7]



					# SPECIFY ROI 
					tsf_frame[75:195, 125:245] = cv2.cvtColor(question_s[shape_test_i][0], cv2.COLOR_GRAY2RGB)
					tsf_frame[75:195, 245:365] = cv2. cvtColor(question_s[shape_test_i][1], cv2.COLOR_GRAY2RGB)
					tsf_frame[75:195, 365:485] = cv2. cvtColor(question_s[shape_test_i][2], cv2.COLOR_GRAY2RGB)

					tsf_frame[195:315, 125:245] = cv2. cvtColor(question_s[shape_test_i][3], cv2.COLOR_GRAY2RGB)
					tsf_frame[195:315, 245:365] = cv2. cvtColor(question_s[shape_test_i][4], cv2.COLOR_GRAY2RGB)
					tsf_frame[195:315, 365:485] = cv2. cvtColor(question_s[shape_test_i][5], cv2.COLOR_GRAY2RGB)

					tsf_frame[315:435, 125:245] = cv2. cvtColor(question_s[shape_test_i][6], cv2.COLOR_GRAY2RGB)
					tsf_frame[315:435, 245:365] = cv2. cvtColor(question_s[shape_test_i][7], cv2.COLOR_GRAY2RGB)
	


					result = []

					white, black, bNw, result_each = detectors.single_area_checking(block)

					if len(result_each) == 2:
						
						result.append(result_each)
						shape_result = result_each[0][0]
						angle_result = result_each[1][0]
						
						show_1[:,:] = pattern_storage[shape_result - 1][angle_result]

		
					#print result

					# SET BACKGROUND COLOR
					tsf_frame[0:w, 0:125] = background_color
					tsf_frame[0:75, 125:h] = background_color
					tsf_frame[435:w, 125:485] = background_color
					tsf_frame[75:w, 485:h] = background_color




				cv2.imshow('show_screen', show_screen)
				cv2.imshow('tsf_frame',tsf_frame)		
				#cv2.imshow('block', block)
				#cv2.imshow('white',white)
				#cv2.imshow('bNw',bNw)


				end_time = time.clock()
				during_time = end_time - start_time

				switch = cv2.waitKey(1) & 0xFF

				if switch == ord('s') or during_time > 60:
					print 'Shape-matching Test',shape_test_i+1,'is checking'
					#print result, answer_s[shape_test_i]


					if result == answer_s[shape_test_i]:
						print 'correct'
						print 'time =', during_time

					else:
						print 'wrong'

					shape_test_i += 1
					break

				elif switch == ord('q'):
					exit()

				elif switch == ord('a'):
					shape_test_i -= 1



	else:
		print 'Wrong Selection'

cap.release()
cv2.destroyAllWindows()

