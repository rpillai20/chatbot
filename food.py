import requests
import re

r = requests.post('https://www.myschooldining.com/groton/calendarMonth', data={'current_month':'2019-01-16','adj':'0'})
data=r.text
data = data.replace("&nbsp;","")
regex = re.compile("<div class='.*?' day_no='\d*' id='\d*' this_date='(.*?)'>\s*<div class='day-date'.*?</div>\s*<div.*?>\s*(.*?)\s*</div>", re.DOTALL)
regex2 = re.compile("<span\s*class='month-((?:period)|(?:item))'>\s*(.*?)\s*</span>")
days = regex.findall(data)
[day[0] for day in days]
print(days[23][0])
print()
days[11][1]
menu = regex2.findall(days[23][1])
print(menu)
print(menu[0])
print(menu[0][1])
print()

print([day[0] for day in days])
#print(days[19][1])

bMenu = "Breakfast"
for x in range(1,9):
    food = menu[x][1]
    bMenu += "\n" + food
#print(bMenu) #prints menu

length = len(menu) #20
menuList = ""
for x in range(0,length):
    food = menu[x][1]
    menuList += food + "\n"
print(menuList)

print()
print(menu[0].index('Breakfast'))

print()
print(menu[9])
print(menu[9].index('Lunch'))

# lunchIndex=0
# for x in range(19):
#     if menu[x].index('Lunch')>0:
#         lunchIndex = x
#print(lunchIndex)
i=0
for type,value in menu:
    if value == "Lunch":
        indexLunch = i
        break
    else:
        i+=1
print(indexLunch)

# breakfast = menu.index("Breakfast")
# print(breakfast)
# index = breakfast
# while index<breakfast+5:
#     print(menu[index][1])
#     index+=1
#print(regex2.findall(days[11][1])[0][1])
