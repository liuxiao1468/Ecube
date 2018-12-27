# Ecube Project
# Use the method in computer vision to redevelop sig-block in stead of sensors

# important files
1. camera_calibration_img: images with calibration board.
2. pattern_img: images of block surface patterns (used in the published paper).
3. snapshot: snapshot images (block combination based on the question) used for training and test.
4. tried_approach: the algorithm tested before but not used. 
5. 1block_img.zip: images (1 block only) taken for cascade training and test

# important code
1. perspective_transformation.py: a class to do perspective transformation of the camera.
2. detector.py: a class consists of several detectors, such as black and white color detector, block number detector, shape detector, top surface detector, etc. 
3. main_ecube: the main code for detecting the block type and orientation inside the play area.
4. main_ecube2: defined block displacing area. check the block situation inside the defined area.



