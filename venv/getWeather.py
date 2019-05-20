from bs4 import BeautifulSoup
from pymongo import MongoClient
from collections import OrderedDict
from selenium import webdriver
import requests


client = MongoClient("localhost", 27017)
database = client.test
collection = database.weather



page = "https://new.land.naver.com/complexes?ms=36.6362841,127.471323,10&a=APT:ABYG:JGC&b=A1:B1:B2:B3&e=RETAIL"
path="C:\\chromedriver.exe"
driver = webdriver.Chrome(path)
driver.get(page)
html = driver.page_source


soup = BeautifulSoup(html, 'html.parser')
# general_list = soup.findAll("div", id = "complex_map")
general_list = soup.findAll("a", {"class": "marker_complex--apart"})

for data in general_list:
    price = str()
    consYear = str()


    apart_features = data.findAll("div", {'class' : 'complex_feature'})
    for apart_features in apart_features:
        print(apart_features)

    apart_infos = data.findAll("div", {'class' : 'complex_infos'})
    for apart_info in apart_infos:
        print(apart_info)


    print(data)

# list_of_dl = general_list.find_all("dl")
#
# for in_each_dl in list_of_dl:
#     list_of_dt = in_each_dl.find_all("dt")[0]
#     list_of_dd = in_each_dl.find_all("dd")[1]
#     list_of_alt = in_each_dl.find("img").attrs['alt']
#     data = OrderedDict()
#     data['City'] = list_of_dt.get_text()
#     data['Temperature'] = list_of_dd.get_text()
#     data['Weather'] = list_of_alt
#     print(data)
#     collection.insert(data)
#     # collection.insertOne({"City name: " + list_of_dt.get_text() + ", Temperature: " + list_of_dd.get_text() + ", Weather: " + list_of_alt})
