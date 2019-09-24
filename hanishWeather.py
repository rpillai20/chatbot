import os
from slackclient import SlackClient
from forecastiopy import *

SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
slack_client = SlackClient(SLACK_TOKEN)
DARKSKY_TOKEN = '811e4e0ba6ea577cf92993d06ebc355f'
ZIP_CODE = '01450'
ZIPCODE_DATABASE = path/to/ziplatlon.csv

#groton latitude: 42.6112 N
#groton longitude: 71.5745 W

lat = 42.6112
lng = 71.5745

forecast = forecastio.load_forecast(DARKSKY_TOKEN, lat, lng)

byHour = forecast.hourly()
print (byHour.summary)
print (byHour.icon)
