import os
import time
import requests
import re
import arrow
import sys
from forecastiopy import *
from ics import Calendar
from urllib.request import urlopen
from arrow import Arrow
from ics.timeline import Timeline
from dateutil import tz
from datetime import datetime

from slackclient import SlackClient
sc = SlackClient("xoxb-425105090817-494178107058-i2scia60wUVgJVEJtqdEcoYD")
#slack_token = os.environ["SLACK_TOKEN"]

def sendMessage(response):
    sc.api_call(
      "chat.postMessage",
      channel="CEMSF3CJ1",
      text=response
      )

def getJoke():
    resp=requests.get('https://official-joke-api.appspot.com/random_joke')
    setup = resp.json()['setup']
    punchline = resp.json()['punchline']
    return(setup+" "+punchline)

def getWeather():
    DARKSKY_TOKEN = "811e4e0ba6ea577cf92993d06ebc355f"
    lat = 42.6112
    lng = 71.5745
    fio = ForecastIO.ForecastIO(DARKSKY_TOKEN, latitude=lat, longitude=lng)
    current = FIOCurrently.FIOCurrently(fio)
    weather = "The weather right now in Groton, MA is:"
    weather += '\nTemperature: '+ str(current.temperature)
    weather += '\nPrecipitation Probability: '+ str(current.precipProbability)
    return weather

def dateFinder(message):
    regex = re.compile("(\d\d)/(\d\d)/(\d\d\d\d)")
    m = regex.search(message)
    if m:
        return m.groups()
    elif message.lower().count("tomorrow")>0:
        return "tomorrow"
    elif message.lower().count("yesterday")>0:
        return "yesterday"
    else:
        return False

def mealFinder(message):
    if message.lower().count("breakfast")>0:
        return "breakfast"
    elif message.lower().count("lunch")>0:
        return "lunch"
    elif message.lower().count("dinner")>0:
        return "dinner"

def getMenu(date,month,year):
    #r = requests.post('https://www.myschooldining.com/groton/calendarMonth', data={'current_month':'2019-01-16','adj':'0'})
    r = requests.post('https://www.myschooldining.com/groton/calendarMonth', data={'current_month':'%d-%d-%d' %(year,month,date),'adj':'0'})
    data=r.text
    data = data.replace("&nbsp;","")
    regex = re.compile("<div class='.*?' day_no='\d*' id='\d*' this_date='(.*?)'>\s*<div class='day-date'.*?</div>\s*<div.*?>\s*(.*?)\s*</div>", re.DOTALL)
    regex2 = re.compile("<span\s*class='month-((?:period)|(?:item))'>\s*(.*?)\s*</span>")
    days = regex.findall(data)
    [day[0] for day in days]
    menu = regex2.findall(days[date-1][1])
    length = len(menu)
    menuList = ""
    for x in range(0,length):
        food = menu[x][1]
        menuList += food + "\n"
    return(menuList)

def getBreakfast(date,month,year):
    menu = getMenu(date,month,year)
    lunchIndex = menu.index("Lunch")
    print(lunchIndex)
    return menu[0:lunchIndex-1]

def getLunch(date,month,year):
    menu = getMenu(date,month,year)
    lunchIndex = menu.index("Lunch")
    dinnerIndex = menu.index("Dinner")
    return menu[lunchIndex:dinnerIndex-1]

def getDinner(date,month,year):
    menu = getMenu(date,month,year)
    dinnerIndex = menu.index("Dinner")
    end = len(menu)
    return menu[dinnerIndex:end]

def getCalendar(date,month,year):
    url = """https://groton.myschoolapp.com/podium/feed/iCal.aspx?z=3i2couATjUdOUCGFhn1E7yD20PGirIkkdTaH6NKG5trwUSCtY9TsDuKqBlphNBFrlKcgnGwwSlPnMZeknEiwwQ%3d%3d"""
    c = Calendar(urlopen(url).read().decode('iso-8859-1'))
    t = Timeline(c)
    cal = [e for e in t.on(arrow.get(datetime(year, month, date), tz.gettz('US/Eastern')),strict=True)]
    length = len(cal)
    events = ""
    for x in range (0,length):
        name = cal[x].name
        hour = cal[x].begin.hour
        minute = cal[x].begin.minute
        if(minute==0):
            minute="00"
        if(hour>12):
            hour = hour - 12
            events += str(hour) + ":" + str(minute) + " PM - " + str(name) + "\n"
        else:
            events += str(hour) + ":" + str(minute) + " AM - " + str(name) + "\n"
    return events


if sc.rtm_connect():
    sendMessage("------------------------------------------------------------------------")
    sendMessage("Hi! I am the Groton slack bot! Ask me for: \n-Jokes \n-The menu [with date (mm/dd/yyyy) or meal name] \n-The current weather (Groton, MA) \n-The calendar (whole school)")
    sendMessage("------------------------------------------------------------------------")
    while sc.server.connected is True:
        d =sc.rtm_read()
        if len(d)>0 and 'text' in d[0].keys() and 'user' in d[0].keys():
            user = d[0]['user']
            response = "I'm sorry, I don't understand."
            message = d[0]['text']
            if message.lower().count("joke")>0:
                response = getJoke()
            elif message.lower().count("hi")>0 or message.lower().count("hello")>0:
                response = "Hi!"
            elif message.lower().count("how are you")>0 or message.lower().count("what's up")>0:
                response = "I'm good! How are you?"
            elif message.lower().count("good")>0 or message.lower().count("great")>0:
                response = "I'm glad!"
            elif message.lower().count("thank")>0:
                response = "You're welcome!"
            elif message.lower().count("weather")>0:
                response = getWeather()
            elif message.lower().count("menu")>0:
                date = dateFinder(message)
                if not date:
                    day = arrow.now().date().day
                    month = arrow.now().date().month
                    year = arrow.now().date().year
                elif dateFinder(message)=="tomorrow":
                    utc = arrow.utcnow()
                    utc = utc.replace(days=+1)
                    day = utc.date().day
                    month = utc.date().month
                    year = utc.date().year
                elif dateFinder(message)=="yesterday":
                    utc = arrow.utcnow()
                    utc = utc.replace(days=-1)
                    day = utc.date().day
                    month = utc.date().month
                    year = utc.date().year
                else:
                    day = int(date[1])
                    month = int(date[0])
                    year = int(date[2])
                print(month," ",day," ",year)
                print(mealFinder(message))
                if mealFinder(message)=="breakfast":
                    response = getBreakfast(day,month,year)
                elif mealFinder(message)=="lunch":
                    response = getLunch(day,month,year)
                elif mealFinder(message)=="dinner":
                    response = getDinner(day,month,year)
                else:
                    response = getMenu(day,month,year)
            elif message.lower().count("calendar")>0:
                date = dateFinder(message)
                if not date:
                    day = arrow.now().date().day
                    month = arrow.now().date().month
                    year = arrow.now().date().year
                elif dateFinder(message)=="tomorrow":
                    utc = arrow.utcnow()
                    utc = utc.replace(days=+1)
                    day = utc.date().day
                    month = utc.date().month
                    year = utc.date().year
                elif dateFinder(message)=="yesterday":
                    utc = arrow.utcnow()
                    utc = utc.replace(days=-1)
                    day = utc.date().day
                    month = utc.date().month
                    year = utc.date().year
                else:
                    day = int(date[1])
                    month = int(date[0])
                    year = int(date[2])
                print(month," ",day," ",year)
                response = getCalendar(day,month,year)
            if(response==""):
                response = "I'm sorry, there are no results for that request."

            sendMessage(response)
        #time.sleep(3)

else:
    print ("Connection Failed")
