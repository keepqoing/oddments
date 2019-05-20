from bs4 import BeautifulSoup
from matplotlib import font_manager, rc
import matplotlib.pyplot as plt
from pymongo import MongoClient
import requests
import operator


page = requests.get("http://www.naver.com")
soup = BeautifulSoup(page.content, 'html.parser')
title = soup.find('title')

client = MongoClient("localhost", 27017)
database = client.test
# collection = database.weather
# docs = collection.find().sort('Temperature')

collection = database.portal4

pipeline = list()

pipeline.append({'$group' : { '_id' : '$day', 'count' : {'$sum' : 1}}})
pipeline.append({'$sort' : {'count' : -1}})
pipeline.append({'$'})

docs = collection.find().sort('Temperature')

city = list()
temp = list()

for doc in docs:
    city.append(doc['City'])
    temp.append(doc['Temperature'])

print(city)
print(temp)


font_name = font_manager.FontProperties(fname = "C:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family = font_name)

title = 'City - Temperature'
xlab = 'Temperature'
ylab = 'City'
plt.xlabel(xlab)
plt.ylabel(ylab)
plt.title(title)

plt.plot(city,temp)
plt.show()