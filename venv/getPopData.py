from bs4 import BeautifulSoup
from pymongo import MongoClient
from collections import OrderedDict
import requests
from random import *
from selenium import webdriver

client = MongoClient("localhost", 27017)
database = client.test
collection = database.world_pop

url = "https://www.worldometers.info"
page =  "/population/"

# Since the table showing the data is added dynamically after loading the JavaScript,
# use the selenium module additionally.
path="C:\\chromedriver.exe"
driver = webdriver.Chrome(path)
driver.get(url + page)
html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')
content_div = soup.find("div", {"class": "content-inner"})

# The items I want to crawl are in the last ul tag.
ul_list = content_div.findAll("ul")
object_ul = ul_list[len(ul_list)-1]

# the <a> tags in this ul contains the link of the page that displays each country's population informatio
countryLink_a_list = object_ul.findAll("a")

countryPages = []
for countryLink_a in countryLink_a_list:
    countryPages.append(countryLink_a["href"])


# A for loop that crawls and stores data for each country page
for countryPage in countryPages:
    # Dictionary to be stored in MongoDB database
    countryData = {}
    countryPage = countryPage.replace("http", "https")

    page = requests.get(url + countryPage, timeout=5)

    soup = BeautifulSoup(page.content, 'html.parser')

    # Get the continentName, regionName, countryName in the breadcrumb class ul.
    # Each of items are in the 3rd to 5th <li> tags.
    countryInfo = soup.find("ul", {"class" : "breadcrumb"})
    countryInfo_li = countryInfo.findAll("li")

    continentName = countryInfo_li[3].get_text()
    countryData['continentName'] = continentName

    # Exception handling
    if continentName == 'Northern America':
        regionName = 'Northern America'
        countryName = countryInfo_li[4].get_text()
        countryData['countryName'] = countryName
    else:
        regionName = countryInfo_li[4].get_text()
        if regionName == "Micronesia":
            continue

        countryData['regionName'] = regionName
        countryName = countryInfo_li[5].get_text()
        countryData['countryName'] = countryName

    print(continentName, regionName, countryName)
    # historical_Data and forecast_Data are the array of documents to be stored in the countryData document.
    countryData['historical_Data'] = []
    countryData['forecast_Data'] = []

    # The fields that is to be contained to historical_Data and forecast_Data
    fields = ['year', 'population', 'yearlyChangePer', 'yearlyChange', 'migrants', 'medianAge', 'fertilityRate',
               'density', 'urbanPopPer', 'urbanPop', 'shareOfWorldPop', 'worldPopulation', 'globalRank']

    # Get the historical_Data, forecast_Data data table in the table table-striped table-bordered table-hover table-condensed table-list class.
    # The historical_Data is contained to the first table.
    tables = soup.findAll("table", {"class" : "table table-striped table-bordered table-hover table-condensed table-list"})
    population_historical = tables[0]
    print(population_historical)

    tbody = population_historical.find("tbody")
    tr_list = tbody.findAll("tr")

    for tr in tr_list:
        td_list = tr.findAll("td")
        historical_data = {}
        for index, td in enumerate(td_list):
            historical_data[fields[index]] = td.get_text()

        countryData['historical_Data'].append(historical_data)
        print(historical_data)

    # The forecast_Data is contained to the second table.
    population_forecast = tables[1]
    print(population_forecast)

    tbody = population_forecast.find("tbody")
    tr_list = tbody.findAll("tr")

    for tr in tr_list:
        td_list = tr.findAll("td")
        forecast_data = {}
        for index, td in enumerate(td_list):
            forecast_data[fields[index]] = td.get_text()

        countryData['forecast_Data'].append(forecast_data)
        print(forecast_data)

    print(countryData)

    # Store the countryData into the MongoDB collection.
    collection.insert_one(countryData)


