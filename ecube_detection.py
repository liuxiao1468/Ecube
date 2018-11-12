import cv2
import numpy as np
import os

def detect_ecube_from_webcam():
    #ecube_cascade=cv2.CascadeClassifier('1block.xml')
    ecube_cascade=cv2.CascadeClassifier('cascade.xml')
    cap = cv2.VideoCapture(0)

        
    while(True):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        ecube=ecube_cascade.detectMultiScale(gray,10,300)
        for (x,y,w,h) in ecube:
            cv2.rectangle(frame,(x,y),(x+2*w,y+2*h),(255,0,0),2) # the image to draw, starting point, ending point, color, line thickness.
        
        cv2.imshow('frame',frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


    
def detect_ecube_from_image():
    ecube_cascade=cv2.CascadeClassifier('cascade.xml')
    img_path= '/home/liutao/ecube/snapshot/4.jpg'
    img=cv2.imread(img_path)
    gray_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ecube=ecube_cascade.detectMultiScale(gray_img,500,500)
    for (x,y,w,h) in ecube:
        print 'X coordinate:', x
        print 'Y coordinate:', y
        print 'Width:', w
        print 'Height:',h
        cv2.rectangle(img,(x,y),(x+2*w,y+2*h),(255,0,0),2) # the image to draw, starting point, ending point, color, line thickness.
        font=cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img,'ecube',(x,y-5),font,0.4,(200,255,255),1,cv2.LINE_AA)
    cv2.imshow('ecube',img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()



#detect_ecube_from_image()
detect_ecube_from_webcam()
