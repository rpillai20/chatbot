import os
import time
import requests
import re
import arrow
from forecastiopy import *
import sys
from slackclient import SlackClient
#importing all the things from chatbot
#made to test the date functions of arrow that are in the chatbot
print(arrow.now().date().day)
print(arrow.now().date())
print(arrow.now().date().month)
print(arrow.now().time())
print()

#dir(arrow)
#dir(arrow.now())

#yesterday
utc = arrow.utcnow()
utc = utc.replace(days=-1)
print(utc)
print(utc.date().day)
print(utc.date().month)
print(utc.date().year)
print()

#tomorrow
utc = arrow.utcnow()
utc = utc.replace(days=+1)
print(utc)
print(utc.date().day)
print(utc.date().month)
print(utc.date().year)
