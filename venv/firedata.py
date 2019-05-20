import csv
import xml.etree.ElementTree as ET
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests

API_HOST = 'http://openapi.forest.go.kr'
headers = {'Authorization': 'Bearer [YOUR_ACCESS_TOKEN]'}


def req(path, query, method, data={}):
    url = API_HOST + path

    if method == 'GET':
        return requests.get(url, headers=headers)
    else:
        return requests.post(url, headers=headers, data=data)


f = req(
    '/openapi/service/forestDisasterService/frstFireOpenAPI?serviceKey=5u5cqrL38pQrvbgYZWYU0EqtJQEYlSqSBLe4r%2F0%2BTx7ZajQ0pu1eXkx%2BWzgl1Xp8wmS9vlTd0SEJFx7FRSvlyA%3D%3D&searchStDt=19700101&searchEdDt=20190408&pageNo=1&numOfRows=10000000',
    '', 'GET')
# print(f.text)
data = ET.fromstring(f.text)
# print(data)

tmp = data.find('body')
print(tmp)
lst = tmp.findall('items/item')  # XML트리에서 nations/nation안의 subtrees를 불러온다
print('The number of items:', len(lst))  # nation이 몇 개인지 출력

with open('firedata.csv','w',encoding='utf-8', newline='') as after:
    fieldName = ["ocurdt","ocuryoil","extingdt","exintgtm","ocurgm", "ocurdo","ocursgg","ocuremd","ocurri","ocurjibun","ownersec","ocurcause",
                 "dmgarea","dmgmoney","riskavg","riskmax","tempavg","humidcurr","humidrel","humidmin","windmax","windavg","dirmax","diravg","raindays","rainamount"]
    writer = csv.DictWriter(after,fieldnames=fieldName)
    writer.writeheader()
    for item in lst:
        row = {}
        row["ocurdt"] = item.find('ocurdt').text
        row["ocuryoil"] = item.find('ocuryoil').text
        row["extingdt"] = item.find('extingdt').text
        row["exintgtm"] = item.find('exintgtm').text
        row["ocurgm"] = item.find('ocurgm').text
        row["ocurdo"] = item.find('ocurdo').text
        row["ocursgg"] = item.find('ocursgg').text
        row["ocuremd"] = item.find('ocuremd').text
        row["ocurri"] = item.find('ocurri').text
        row["ocurjibun"] = item.find('ocurjibun').text
        row["ownersec"] = item.find('ownersec').text
        row["ocurcause"] = item.find('ocurcause').text
        row["dmgarea"] = item.find('dmgarea').text
        row["dmgmoney"] = item.find('dmgmoney').text
        row["riskavg"] = item.find('riskavg').text
        row["riskmax"] = item.find('riskmax').text
        row["tempavg"] = item.find('tempavg').text
        row["humidcurr"] = item.find('humidcurr').text
        row["humidrel"] = item.find('humidrel').text
        row["humidmin"] = item.find('humidmin').text
        row["windmax"] = item.find('windmax').text
        row["windavg"] = item.find('windavg').text
        row["dirmax"] = item.find('dirmax').text
        row["diravg"] = item.find('diravg').text
        row["raindays"] = item.find('raindays').text
        row["rainamount"] = item.find('rainamount').text
        writer.writerow(row)

# with open('after5.csv','w', newline='') as after:
#     # fieldName = ["old_tapPos", "new_tapPos", "stayTime"]
#     fieldName = ["old_tapPos","new_tapPos","sTime","eTime","stayTime", "ElePower","ampereA1","ampereB1","ampereC1","ampereA2","ampereB2","ampereC2",
#                  "voltageA1","voltageB1","voltageC1","voltageA2","voltageB2","voltageC2","pfA","pfB","pfC","epiA","epiB","epiC","trTemp"]
#     writer = csv.DictWriter(after,fieldnames=fieldName)
#     writer.writeheader()
#
#     with open('2weeks.csv', newline='') as f:
#         rdr = csv.DictReader(f)
#         old_tapPos = 0
#         sTime = 0
#         eTime = 0
#         count = 0
#         rownum = 0
#         tmplist = dict()
#         tmpkeys = []
#
#         for data in rdr:
#             if (rownum == 0):
#                 tmp = dict(data)
#                 tmpkeys = tmp.keys()
#
#
#                 print(tmp.keys())
#                 rownum = 1
#                 old_tapPos = data['tapPos']
#                 sTime = data['dates']
#                 eTime = data['dates']
#
#                 for index in tmp:
#                     tmplist[index] = []
#                     tmplist[index].append(data[index])
#
#             else:
#                 new_tapPos = data['tapPos']
#                 if (old_tapPos != new_tapPos):
#                     sTime2 = datetime(int(sTime[0:4]), int(sTime[4:6]), int(sTime[6:8]), int(sTime[8:10]),
#                                      int(sTime[10:12]), int(sTime[12:14]))
#                     eTime2 = datetime(int(eTime[0:4]), int(eTime[4:6]), int(eTime[6:8]), int(eTime[8:10]),
#                                      int(eTime[10:12]), int(eTime[12:14]))
#                     stayTime = (eTime2 - sTime2).seconds
#
#                     if(stayTime > 600):
#                         row = {}
#                         row["old_tapPos"] = old_tapPos
#                         row["new_tapPos"] = new_tapPos
#                         row["sTime"] = sTime2
#                         row["eTime"] = eTime2
#                         row["stayTime"] = stayTime
#                         row["ElePower"] = np.median(np.array(tmplist['avgElePower']).astype(np.float))
#                         row["ampereA1"] = np.median(np.array(tmplist['ampereA1']).astype(np.float))
#                         row["ampereA1"] = np.median(np.array(tmplist['ampereA1']).astype(np.float))
#                         row["ampereB1"] = np.median(np.array(tmplist['ampereB1']).astype(np.float))
#                         row["ampereC1"] = np.median(np.array(tmplist['ampereC1']).astype(np.float))
#                         row["ampereA2"] = np.median(np.array(tmplist['ampereA2']).astype(np.float))
#                         row["ampereB2"] = np.median(np.array(tmplist['ampereB2']).astype(np.float))
#                         row["ampereC2"] = np.median(np.array(tmplist['ampereC2']).astype(np.float))
#                         row["voltageA1"] = np.median(np.array(tmplist['voltageA1']).astype(np.float))
#                         row["voltageB1"] = np.median(np.array(tmplist['voltageB1']).astype(np.float))
#                         row["voltageC1"] = np.median(np.array(tmplist['voltageC1']).astype(np.float))
#                         row["voltageA2"] = np.median(np.array(tmplist['voltageA2']).astype(np.float))
#                         row["voltageB2"] = np.median(np.array(tmplist['voltageB2']).astype(np.float))
#                         row["voltageC2"] = np.median(np.array(tmplist['voltageC2']).astype(np.float))
#                         row["pfA"] = np.median(np.array(tmplist['pfA']).astype(np.float))
#                         row["pfB"] = np.median(np.array(tmplist['pfB']).astype(np.float))
#                         row["pfC"] = np.median(np.array(tmplist['pfC']).astype(np.float))
#                         row["epiA"] = np.median(np.array(tmplist['epiA']).astype(np.float))
#                         row["epiB"] = np.median(np.array(tmplist['epiB']).astype(np.float))
#                         row["epiC"] = np.median(np.array(tmplist['epiC']).astype(np.float))
#                         row["trTemp"] = np.median(np.array(tmplist['trTemp']).astype(np.float))
#                         # print(row)
#                         writer.writerow(row)
#                         for index in tmpkeys:
#                             tmplist[index].clear()
#                         old_tapPos = new_tapPos
#                         sTime = data['dates']
#                         eTime = data['dates']
#                     else:
#                         eTime = data['dates']
#
#
#
#                 else:
#                     for index in tmpkeys:
#                         tmplist[index].append(data[index])
#                         eTime = data['dates']
#
#
#
#
#
#
