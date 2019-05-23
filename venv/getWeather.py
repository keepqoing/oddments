from bs4 import BeautifulSoup
from pymongo import MongoClient
from collections import OrderedDict
import requests
import time
from random import *

client = MongoClient("localhost", 27017)
database = client.test
collection = database.world_pop


url = "https://www.worldometers.info"
page =  "/population/"

page = requests.get(url + page, timeout=5)

soup = BeautifulSoup(page.content, 'html.parser')
# general_list = soup.findAll("div", id = "complex_map")
div = soup.findAll("div", {"class": "content-inner"})
print(div)

ul_list = div.findAll("ul")
countryLink_ul = ul_list[len(ul_list) - 1]

countryLink_a_list = countryLink_ul.findAll("a")


countryPages = []
for countryLink_a in countryLink_a_list:
    countryPages.append(countryLink_a["href"])

print(countryPages)


#
#
#
# continentPages = []
#
# for continent in continents:
#     continentPage = continent.find("a")["href"]
#     continentPages.append(continentPage)
#
# countryPages = []
#
# for continentPage in continentPages:
#     page = requests.get(url + continentPage, timeout=5)
#     soup = BeautifulSoup(page.content, 'html.parser')
#     countries = soup.findAll("div", {"class": "noli"})
#
#     for country in countries:
#         countryLis = country.findAll("li")
#
#         for index, countryLi in enumerate(countryLis):
#             if index == 0:
#                 continue
#             countryPage = countryLi.find("a")["href"]
#             countryPages.append(countryPage)
#
# for countryPage in countryPages:
#     print(countryPage)
#
# for countryPage in countryPages:
#     countryData = {}
#     countryPage = countryPage.replace("http", "https")
#     if url in countryPage:
#
#         print("url in countryPage")
#         print(countryPage)
#         page = requests.get(countryPage, timeout=5)
#
#     else:
#         print(url + countryPage)
#         page = requests.get(url + countryPage, timeout=5)
#
#
#     soup = BeautifulSoup(page.content, 'html.parser')
#
#     countryInfo = soup.find("ul", {"class" : "breadcrumb"})
#     countryInfo_li = countryInfo.findAll("li")
#
#     continentName = countryInfo_li[3].get_text()
#     regionName = countryInfo_li[4].get_text()
#     countryName = countryInfo_li[5].get_text()
#
#     countryData['continentName'] = continentName
#     countryData['regionName'] = regionName
#     countryData['countryName'] = countryName
#     countryData['historical_Data'] = []
#     countryData['forecast_Data'] = []
#
#     print(continentName,regionName, countryName)
#
#     tables = soup.findAll("table", {"class" : "table table-striped table-bordered table-hover table-condensed table-list"})
#     population_historical = tables[0]
#     print(population_historical)
#
#     thead = population_historical.find("thead")
#     th_list = thead.findAll("th")
#
#     columns = []
#     for th in th_list:
#         columns.append(th.get_text())
#     print(columns)
#
#     tbody = population_historical.find("tbody")
#     tr_list = tbody.findAll("tr")
#
#
#     for tr in tr_list:
#         td_list = tr.findAll("td")
#         historical_data = {}
#         for index, td in enumerate(td_list):
#             # print(columns[index], " : ", td.get_text())
#             historical_data[columns[index]] = td.get_text()
#
#         countryData['historical_Data'].append(historical_data)
#         print(historical_data)
#
#
#     population_forecast = tables[1]
#     print(population_forecast)
#     tbody = population_forecast.find("tbody")
#     tr_list = tbody.findAll("tr")
#
#
#     for tr in tr_list:
#         td_list = tr.findAll("td")
#         forecast_data = {}
#         for index, td in enumerate(td_list):
#             # print(columns[index], " : ", td.get_text())
#             forecast_data[columns[index]] = td.get_text()
#
#         countryData['forecast_Data'].append(forecast_data)
#         print(forecast_data)
#
#     print(countryData)
#     collection.insert_one(countryData)
#
#     # rand_value = randint(1, 10)
#     # time.sleep(rand_value)
