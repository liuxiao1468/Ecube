import picamera
import picamera.array
from time import sleep
import cv2

camera = picamera.PiCamera()

camera.resolution = (1024,768)
#camera.resolution = (640,480)
camera.framerate = 64
rawCapture = picamera.array.PiRGBArray(camera,size=(1024,768))
camera.crop = (0.25, 0.25, 0.5, 0.5)
sleep(0.1)

for frame in camera.capture_continuous(rawCapture,format='bgr',use_video_port=True):
    image = frame.array
    
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=1.8, tileGridSize=(3,3))
    cl = clahe.apply(gray)
    blur = cv2.blur(cl,(6,6))
    _,mask1 = cv2.threshold(blur,200,255,cv2.THRESH_BINARY)

    img,contours,hierarchy = cv2.findContours(mask1,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    #cnt = contours[0]
    cv2.drawContours(img,contours,-1,100,3)

    cv2.imshow('frame',img)
    
    rawCapture.truncate(0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    


#camera.start_preview()

#sleep(30)
#camera.stop_preview()
