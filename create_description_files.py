import os
import cv2
import numpy as np

def create_neg_description_files():
    for img in os.listdir('neg'):
        line= 'neg/'+img+'\n'
        with open('test.txt','a') as f:
            f.write(line)

def create_neg_description_files_modified():
    for img in os.listdir('neg'):
        line= 'neg/'+img+'\n'
        open('bg.txt','a').write(line)

def create_pos_description_files():
    for img in os.listdir('resized_ecube'):
        line = img + ' 1 0 0 50 50\n'
        #print line
        open('info.lst','a').write(line)
         

        
create_neg_description_files_modified()
#create_pos_description_files()
