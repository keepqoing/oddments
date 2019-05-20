import csv
import json
from collections import OrderedDict
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


keys = []
result = []

with open('D:\\portal2.csv', encoding='utf-8-sig', newline='') as f:
    print("key list 만드는중...")

    rdr = csv.DictReader(f)
    i = 0
    ip = str()

    for data in rdr:
        ip = data['ip']
        # i += 1

        if ip not in keys:
            keys.append(ip)
            oneData = OrderedDict()
            oneData['search'] = []
            result.append(oneData)

            # if i == 1000:
            #     print(result)
            #     break

print("key list 생성 완료")
keys.sort()

with open('D:\\portal2.csv', encoding='utf-8-sig', newline='') as f:
    print("json으로 만드는중...")
    rdr = csv.DictReader(f)
    i = 0
    ip = str()
    for data in rdr:
        # print(data)
        ip = data['ip']
        if ip not in  result[keys.index(ip)].keys():
            result[keys.index(ip)]['ip'] = ip
        da = OrderedDict()
        # date: 2016 - 11 - 120: 00,
        # datetime: 2016 - 11 - 124: 52,
        # url: 'search',
        # host: 'google.com',
        # sWord: '페이스북상태',
        # sWord_Spacing: ['페이스북', '상태']
        # timetmp = data['날짜시간']
        # sDate = datetime(int(timetmp[0:4]), int(timetmp[5:7]), int(timetmp[8:10]), int(timetmp[11:13]),
        #                   int(timetmp[14:16]), int(timetmp[17:19]))
        da['date'] = data['datetime']
        da['day'] = data['day']
        da['url'] = data['url']
        da['host'] = data['host']
        da['sWord'] = data['sWord']
        da['sWordSpace'] = str(data['sWord_Spacing']).split(' ')
        # print(da)

        result[keys.index(ip)]['search'].append(da)
        # i += 1
        # if i == 1000:
        #
        #     print(result)
        #     break

    with open('portal_Search.json', 'w', encoding="utf-8") as make_file:
        json.dump(result, make_file, ensure_ascii=False, indent="\t")
