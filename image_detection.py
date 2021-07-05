# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 11:43:46 2021

@author: JAY KISHAN OMAR
"""

import requests
import io
import json
import pyttsx3
import cv2
import numpy as np
import matplotlib.pyplot as plt
from keras.models import load_model
from time import sleep
import time
import os
from twilio.rest import Client


net = cv2.dnn.readNet("yolov3_my.weights", "yolov3_my.cfg")
classes = []


with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
    
layers = net.getLayerNames()
output_layers = [layers[i[0]-1] for i in net.getUnconnectedOutLayers()]

print(classes)
print(output_layers)


def get_image():
    cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")
    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, None, fx=1.0, fy=1.0, interpolation=cv2.INTER_AREA)
        cv2.imshow("Guessing Window", frame)
        img = frame
        cv2.imwrite("C:/Users/Dell/Desktop/EduSense/imge.jpg",img)
        #img = cv2.imread("C:/Users/Dell/Desktop/EduSense/imge.jpg")
        height, width, _= img.shape
        
        c = cv2.waitKey(1)
        if c == 32:
            break
    cap.release()
    return img

colors = np.random.uniform(0, 255, size = (len(classes), 3))
image = get_image()
image = cv2.resize(image, None, fx = 1.0, fy = 1.0)
height, width, channels = image.shape
print(height, width)

blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0,0,0), True, crop = False)

#for the representation of blob
#for b in blob:
#    for n,image_blob in enumerate(b):
#        cv2.imshow(str(n), image_blob)

        
net.setInput(blob)
outs = net.forward(output_layers)

boxes = []
confidences = []
class_ids = []



for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence>0.5:
            center_x = int(detection[0]*width)
            center_y = int(detection[1]*height)
            w = int(detection[2]*width)
            h = int(detection[3]*height)
            x = int(center_x - w/2)
            y = int(center_y - h/2)
            boxes.append([x,y,w,h])
            confidences.append(float(confidence))
            class_ids.append(class_id)

            

object = []
indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)            
for i in range(len(boxes)):
    if i in indexes:
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        color = colors[i]
        cv2.circle(image, (center_x, center_y), 10, color, 2)
        cv2.rectangle(image, (x,y), (x+w, y+h), color, 2)
        cv2.putText(image, label, (x,y+2), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
        object.append(label)
        
        
object_set = set(object)
plt.imshow(image)        
cv2.imshow("image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()



def my_speak_cloud(my_message):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate)
    engine.say('{}'.format(my_message))
    engine.runAndWait()

person_count = 0
for message in object_set:
    print(message)
    if(message == "person"):
        person_count = 1
        my_speak_cloud(message)
    else:
        my_speak_cloud(message)
        

REV_CLASS_MAP = {
    0: "jay",
    1: "sammy",
    2: "stranger"
}
model = load_model("drishti-model3(new).h5")

def mapper(val):
    return REV_CLASS_MAP[val]

message = ""
name = ""
def get_message(name):
    if name == "jay":
        message = "Hello jay"
    elif name == "sammy":
        message = "Hello sammy"
    else:
        message = "Not able to recognize"
    return message

start_time = time.time()        
if person_count == 1:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot open webcam")
    while True:
        ret, frame = cap.read()
        cv2.rectangle(frame, (100, 100), (500, 500), (255, 255, 255), 2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        # rectangle for computer to play
        # extract the region of image within the user rectangle
        #roi = frame[100:500, 100:500]
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (300, 300))
        pred = model.predict(np.array([img]))
        val = np.argmax(pred[0])
        if val!=0 and val!=1:
            val = 2
        name = mapper(val)
        #cv2.putText(frame, "Name: " + name,
        #        (500, 50), font, 1.2, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow("Update", frame) 
        if time.time()-start_time>12:
            cap.release()
            break

print(name)    
msg = get_message(name)
print(msg) 
my_speak_cloud(msg)

cv2.waitKey(0)
cv2.destroyAllWindows()


if(name=="stranger"):
    res = requests.get('https://ipinfo.io/')
    data = res.json()
    city = data['city']
    location = data['loc'].split(',')
    latitude = location[0]
    longitude = location[1]
    print("city :", city)
    print("latitude :", latitude)
    print("longitude :", longitude)
    location = "city: "+city+" "+"latitude: "+latitude+" "+"longitude: "+longitude
    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    #account_sid = os.environ['AC28027b89c7b1ec8dece15157f136cfa0']
    #auth_token = os.environ['81a22d50375e99dc92f0991c1837c39d']
    client = Client("AC28027b89c7b1ec8dece15157f136cfa0", "81a22d50375e99dc92f0991c1837c39d")

    message = client.messages \
                    .create(
                        body=location,
                        from_='+18186503477',
                        to=["+917355401152"]
                        )

    print(message.sid)