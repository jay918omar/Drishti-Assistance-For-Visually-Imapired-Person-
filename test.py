# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 11:06:34 2021

@author: TARUN OMAR
"""

from keras.models import load_model
import cv2
import numpy as np
import sys
import matplotlib.pyplot as plt

filepath = r"C:\Users\TARUN OMAR\Desktop\40.jpg"

REV_CLASS_MAP = {
    0: "jay",
    1: "sammy",
    2: "stranger"
}


def mapper(val):
    return REV_CLASS_MAP[val]


model = load_model("drishti-model3(new).h5")

# prepare the image
img = cv2.imread(filepath)
plt.imshow(img)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = cv2.resize(img, (300, 300))

# predict the move made
pred = model.predict(np.array([img]))
move_code = np.argmax(pred[0])
if move_code!=1 and move_code!=0:
    move_code = 2
move_name = mapper(move_code)

print("Predicted: {}".format(move_name))
print(pred)
print(move_code)
print(move_name)