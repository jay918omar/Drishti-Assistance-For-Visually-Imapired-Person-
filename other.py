# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 11:47:18 2021

@author: TARUN OMAR
"""

import cv2
import numpy as np
import requests
import io
import json
import pyttsx3
import matplotlib.pyplot as plt
import os
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content



def my_speak_cloud(my_message):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate)
    engine.say('{}'.format(my_message))
    engine.runAndWait()
img=cv2.imread("control.jpg")
height, width, _ = img.shape
# Cutting image
# roi = img[0: height, 400: width]
roi = img[0:height]

# Ocr
url_api = "https://api.ocr.space/parse/image"
_, compressedimage = cv2.imencode(".jpg", roi, [1, 90])
file_bytes = io.BytesIO(compressedimage)

result = requests.post(url_api,
              files = {"imge.jpg": file_bytes},
              data = {"apikey": "24c92d3ba388957",
                      "language": "eng"})

result = result.content.decode()
result = json.loads(result)

parsed_results = result.get("ParsedResults")[0]
text_detected = parsed_results.get("ParsedText")
print(text_detected)
my_speak_cloud(text_detected)


cv2.imshow("roi", roi)
cv2.imshow("Img", img)
plt.imshow(img)
cv2.waitKey(0)
cv2.destroyAllWindows()

res = requests.get('https://ipinfo.io/')
data = res.json()
city = data['city']
location = data['loc'].split(',')
latitude = location[0]
longitude = location[1]
print("city :", city)
print("latitude :", latitude)
print("longitude :", longitude)


#sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('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'))
#from_email = Email("jaykishan.omar2018@vitstudent.ac.in")  # Change to your verified sender
#to_email = To("tarunbuss918@gmail.com")  # Change to your recipient
#subject = "Location of the user"
#content = Content("text/plain", "Hey, this is the location od the Rahul")
#mail = Mail(from_email, to_email, subject, content)

# Get a JSON-ready representation of the Mail object
#mail_json = mail.get()

# Send an HTTP POST request to /mail/send
#response = sg.client.mail.send.post(request_body=mail_json)
#print(response.status_code)
#print(response.headers)
    
#sendGridApi = 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

