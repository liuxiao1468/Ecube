import os
import cv2
import numpy as np

def resized_pos_image():
    if not os.path.exists('resized_ecube'):
        os.makedirs('resized_ecube')
        
    num_pic=1
    #for img in os.listdir('Closed_vocal_cord_Expansion'):
    for img in os.listdir('corped_ecube'):
        try:
            #img = cv2.imread('Closed_vocal_cord_Expansion/'+img,cv2.IMREAD_GRAYSCALE)
          
            img = cv2.imread('corped_ecube/'+img,0)
            resized_img= cv2.resize(img,(50,50))
            cv2.imwrite('resized_ecube/'+str(num_pic)+'.jpg',resized_img)
            num_pic+=1

        except Exception as e:
            print str(e)


def resized_neg_image():
     
    num_pic=1001
    #for img in os.listdir('Closed_vocal_cord_Expansion'):
    for img in os.listdir('snapshot'):
        try:
            #img = cv2.imread('Closed_vocal_cord_Expansion/'+img,cv2.IMREAD_GRAYSCALE)
          
            img = cv2.imread('snapshot/'+img,0)
            resized_img= cv2.resize(img,(100,100))
            cv2.imwrite('neg/'+str(num_pic)+'.jpg',resized_img)
            num_pic+=1

        except Exception as e:
            print str(e)


#resized_pos_image()
resized_neg_image()

