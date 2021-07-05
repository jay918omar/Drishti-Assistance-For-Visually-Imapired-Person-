# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 14:57:20 2021

@author: TARUN OMAR
"""

import cv2
import os
import tensorflow as tf
import numpy as np
from PIL import Image

count = 0
IMG_READ_PATH = 'image_data'
IMG_SAVE_PATH = 'image_data1'
IMG_CLASS_PATH = os.path.join(IMG_SAVE_PATH, 'converted')
try:
    os.mkdir(IMG_SAVE_PATH)
except FileExistsError:
    pass
try:
    os.mkdir(IMG_CLASS_PATH)
except FileExistsError:
    print("{} directory already exists.".format(IMG_CLASS_PATH))
    print("All images gathered will be saved along with existing items in this folder")
path = os.path.join(IMG_READ_PATH, 'stranger')
print(path)
for item in os.listdir(path):
    # to make sure no hidden files get in our way
    img = cv2.imread(os.path.join(path, item))
    save_path = os.path.join(IMG_CLASS_PATH, '{}.jpg'.format(count + 1))
    cv2.imwrite(save_path, img)
    count += 1
    print(item)
    
            
print("\n{} image(s) saved to {}".format(count, IMG_CLASS_PATH))
