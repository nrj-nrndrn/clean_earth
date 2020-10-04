# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 08:16:34 2020

@author: narendran.n
"""

import pytesseract
import numpy as np
import tkinter as tk
from tkinter import Tk
from tkinter import filedialog
from tkinter import Label
from tkinter import *
import sys,os
from skimage import data, filters
from skimage import color,io
import matplotlib.pyplot as plt
#import imutils
from PIL import Image,ImageTk, ImageChops
import cv2
from PIL import ImageFilter
import colorsys
import glob
import re





os.chdir(r"C:\Users\Public\Documents\hackathon")
img=cv2.imread("Nbill5.jpg")


mask=np.zeros(img.shape[:2],np.uint8)
bgmodel=np.zeros((1,65),np.float64)
fgmodel=np.zeros((1,65),np.float64)
rect=(183,400,1507,3600)
cv2.grabCut(img,mask,rect,bgmodel,fgmodel,2,cv2.GC_INIT_WITH_RECT)
mask2=np.where((mask==2)|(mask==0),0,1).astype('uint8')
img=img*mask2[:,:,np.newaxis]
pts=np.float32([[0,0],[1620,0],[1620,3600],[0,3600]])
rectbox=np.float32([[248,450],[1620,450],[1620,3600],[248,3600]])
op=cv2.getPerspectiveTransform(rectbox,pts)
dst=cv2.warpPerspective(img,op,(1620,3600))
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\narendran.n\AppData\Local\conda\tesseract.exe"
text = pytesseract.image_to_string(dst)

img.show()
new_op = []

''' converting text output into list and removing empty lists'''
sample_list = text.split("\n")
sample_list = [x for x in sample_list if x]

for i, line in enumerate(sample_list):  # for each line in the text_list
    each_item = []
    if '$' in line or '¢' in line:
        if "SUBTOTAL" in line:
            break
        else:

            item_name = ''.join(re.findall(r'[^\d]+ +\w+', line))
            each_item.append(item_name.replace('FN','').strip())  # if each item starts with number code followed by word add to the item list

            if re.search(r'\d@', sample_list[
                i + 1]):  # if text_list next line has number@ that means more than one item is bought
                item_number_str = ''.join(re.findall(r'(\d+)@', sample_list[i + 1]))
                each_item.append(int(item_number_str))
            else:
                if each_item[0] == '':
                    continue
                else:
                    each_item.append(1)  # else only one item is bought

    if each_item != []:
        new_op.append(each_item)  # adding item to the item list



