from bs4 import BeautifulSoup
from pymongo import MongoClient
from collections import OrderedDict
import requests
from random import *
from selenium import webdriver

client = MongoClient("localhost", 27017)
database = client.test
collection = database.world_pop

sWord = "슈퍼문 만의 68년"
sDate = "2016.11.14"
eDate = "2016.11.14"

url = "https://search.naver.com/search.naver?where=news&query="+ sWord +"&sm=tab_opt&sort=0&photo=0&field=0&reporter_article=&pd=3&ds=" + sDate +"&de="+ eDate +"&docid=&nso=so%3Ar%2Cp%3Afrom20161114to20161114%2Ca%3Aall&mynews=0&refresh_start=0&related=0"
# page =  "/population/"

# Since the table showing the data is added dynamically after loading the JavaScript,
# use the selenium module additionally.
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')


news_div = soup.find("div", {"class": "news mynews section _prs_nws"})
news_ul = news_div.find("ul", {"class" : "type01"})
news_li = news_ul.findAll("li")

news_href = []

for news in news_li:
    dd = news.find("dd",{"class" : "txt_inline"})
    if dd:

        a_s = dd.findAll("a", {"class" : "_sp_each_url"})
        if a_s:
            print(dd)
            for a in a_s:
                news_href.append(a['href'])



print(news_href)

for href in news_href:
    print(href)
    page = requests.get(href)
    soup = BeautifulSoup(page.content, 'html.parser')
    articleTitle = soup.find("h3",{"id" : "articleTitle"})
    print("Title")
    print(articleTitle.get_text())
    articleBody = soup.find("div",{"id" : "articleBodyContents"})
    print("contents")
    article_br = articleBody.findAll("br")

    for articleText in article_br:
        print(articleText.get_text())
