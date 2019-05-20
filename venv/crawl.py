import re
from urllib.request import urlopen

import validators
from bs4 import BeautifulSoup

uset = {}
uset['url'] = []

# 사람인 합격스펙 200페이지 분량의 url을 저장
for i in range(1,201):
    uset['url'].append('http://www.saramin.co.kr/zf_user/educe/spec-information/view/page/' + str(i) + '?com_idx=1&tab=list&url=%2Fzf_user%2Feduce%2Fspec-information%3Fpage%3D1%26page_count%3D10%26type%3Dcompany%26listType%3Dgraph&page=1&page_count=5&educe_idx=187'
)

# url으로부터 html을 파싱해 데이터를 추출하는 함수
def getDataFromUrl(uset):
    # 크롤링한 데이터를 저장하는 배열
    dataset = []

    # 미리 저장해둔 url 한개당 한 번씩 반복
    for url in uset['url']:
        # urlopen 모듈을 이용해 url의 html 정보를 가져온다.
        try:
            html = urlopen(url, timeout=10)
            html_data = html.read()
        except:
            return False

        # BeautifulSoup 모듈을 이용해 가져온 html 정보를 파싱
        bsObj = BeautifulSoup(html_data, 'html.parser')
        count = 0
        count2 = 0
        data = []

        # 파싱한 html 정보에서 dd 태그 정보만 사용
        for link in bsObj.findAll('dd'):

            # 필요없는 부분을 걸러내는 코드
            count2 += 1
            if count2 < 8:
                continue

            # 원하는 데이터만 추출
            data.append(str(link).split('>')[1].split('<')[0])
            count += 1
            if count == 11:
                # 한 사람치의 데이터는 11개, 다 차면 최종 데이터셋에 저장
                dataset.append(data)
                data = []
                count = 0

    for i in dataset:
        print(i)
    print(dataset)
    print(len(dataset))

links = getDataFromUrl(uset)

