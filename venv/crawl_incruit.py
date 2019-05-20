import re
from urllib.request import urlopen

import validators
from bs4 import BeautifulSoup

uset = {}
uset['url'] = []

# 인크루트 합격스펙 첫 글의 url
url = 'http://people.incruit.com/community/bbsview.asp?BdNo=134&page=1&cmmno=60718'

# url으로부터 html을 파싱해 데이터를 추출하는 함수
def getDataFromUrl(url):
    # 크롤링한 데이터를 저장하는 배열
    dataset = []

    # 미리 저장해둔 url 한개당 한 번씩 반복
    try:
        html = urlopen(url, timeout = 10)
        html_data = html.read()
    except:
        return False

    bsObj = BeautifulSoup(html_data, 'html.parser')
    detail_info = bsObj.find("div", id="detail_info")
    paragraphs = detail_info.find_all("p")

    for i, p in enumerate(paragraphs):
        pText = str(p).split('>')[1].split('<')[0]
        pText_split = pText.split(':')

        if len(pText_split) != 2:
            continue

        if i < len(paragraphs)-1:
            pText_next = str(paragraphs[i+1]).split('>')[1].split('<')[0]
            pText_next_split = pText_next.split(':')
            if len(pText_next_split) != 2:
                pText_split[1] = pText_split[1] + pText_next_split[0]

        for i in range(0,len(pText_split)):
            pText_split[i] = pText_split[i].strip()
            # pText_split[i] = pText_split[i].replace(" ","")
            pText_split[i] = pText_split[i].replace("\\xa0", "")
            pText_split[i] = pText_split[i].replace(" ","")

        print(pText_split)

        pText_split[0] = pText_split[0].split('. ')[1]




    # for p in paragraphs:
    #     pText = str(p).split('>')[1].split('<')[0]
    #     pText_split = pText.split(':')
    #     print(pText_split)
    #     leftSide = pText_split[0].split('. ')
    #     rightSide = pText_split[1].split(', ')
    #     print(leftSide)
    #     print(rightSide)



links = getDataFromUrl(url)

