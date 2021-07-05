# -*- coding: utf-8 -*-
"""
Created on Sun May 16 20:05:37 2021

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
from twilio.rest import Client


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