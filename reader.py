# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 12:05:57 2021

@author: TARUN OMAR
"""

import cv2
import numpy as np
import requests
import io
import json
import pyttsx3
import matplotlib.pyplot as plt
def my_speak_cloud(my_message):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate)
    engine.say('{}'.format(my_message))
    engine.runAndWait()

cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, None, fx=1.0, fy=1.0, interpolation=cv2.INTER_AREA)
    cv2.imshow('Input', frame)
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #img = cv2.imread("C:/Users/Dell/Desktop/EduSense/imge.jpg")
    height, width, _= img.shape

    c = cv2.waitKey(1)
    if c == 32:
        break

if cap.isOpened():
    ret, frame = cap.read()


else:
    ret = False

# Cutting image
# roi = img[0: height, 400: width]
roi = img

# Ocr
url_api = "https://api.ocr.space/parse/image"
_, compressedimage = cv2.imencode(".jpg", roi, [1, 90])
file_bytes = io.BytesIO(compressedimage)

result = requests.post(url_api,
              files = {"imge.jpg": file_bytes},
              data = {"apikey": "6929d5834c88957",
                      "language": "eng"})

result = result.content.decode()
result = json.loads(result)

parsed_results = result.get("ParsedResults")[0]
text_detected = parsed_results.get("ParsedText")
print(text_detected)
my_speak_cloud(text_detected)


cap.release()
cv2.imshow("roi", roi)
cv2.imshow("Img", img)
cv2.waitKey(0)
cv2.destroyAllWindows()