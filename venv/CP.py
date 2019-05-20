import re
from urllib.request import urlopen

import validators
from bs4 import BeautifulSoup

uset = {}
uset['url'] = []

for i in range(1,201):
    uset['url'].append('http://www.saramin.co.kr/zf_user/educe/spec-information/view/page/' + str(i) + '?com_idx=1&tab=list&url=%2Fzf_user%2Feduce%2Fspec-information%3Fpage%3D1%26page_count%3D10%26type%3Dcompany%26listType%3Dgraph&page=1&page_count=5&educe_idx=187'
)

def getLinksFromUrl(uset):
    links_url = set()
    dataset = []

    for url in uset['url']:
        try:
            html = urlopen(url, timeout=10)
            html_data = html.read()
        except:
            return False

        # print(html_data)
        bsObj = BeautifulSoup(html_data, 'html.parser')
        count = 0
        count2 = 0
        data = []
        for link in bsObj.findAll('dd'):
            count2 += 1
            if count2 < 8:
                continue

            # if count == 0:
                # print("============================================start")
            # print(str(link).split('>')[1].split('<')[0])
            data.append(str(link).split('>')[1].split('<')[0])
            count += 1
            if count == 11:
                # print(data)
                dataset.append(data)
                data = []
                # print("============================================end")
                count = 0

    print(dataset)
    print(len(dataset))

        # for link in bsObj.findAll('table', attrs={'class': 'spec_table'}):
        #
        #     print("============================================start")
        #     print(link.tbody.dd)
        #
        # # if 'href' in link.attrs:
        # #     if not validators.url(link.attrs['href']):
        # #         continue
        # #     links_url.add(link.attrs['href'])
        #     print("============================================end")


    # try:
    #     html = urlopen(uset['url'], timeout=10)
    #     html_data = html.read()
    #     print(html)
    # except:
    #     return False
    #
    # print(html_data)
    # bsObj = BeautifulSoup(html_data, 'html.parser')
    # links_url = set()
    # for link in bsObj.findAll('div', attrs = {'class' : 'spec_detail'}):
    #     print("============================================start")
    #     print(link)
    #
    #     # if 'href' in link.attrs:
    #     #     if not validators.url(link.attrs['href']):
    #     #         continue
    #     #     links_url.add(link.attrs['href'])
    #     print("============================================end")
    #
    #
    #
    #
    # if len(links_url) == 0:
    #     return False
    # else:
    #     return links_url

links = getLinksFromUrl(uset)

