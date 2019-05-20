



import csv
import json
from collections import OrderedDict
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

keys = []
result = []

with open('D:\\portal.csv', encoding='utf-8-sig', newline='') as f:
    rdr = csv.DictReader(f)
    i = 0
    fileNum = 0
    with open('D:\\portal2.csv', 'w', newline='', encoding='utf-8-sig') as after:
        # fieldName = ["old_tapPos", "new_tapPos", "stayTime"]
        fieldName = ["date", "datetime", "day", "ip", "url", "host", "sWord", "sWord_Spacing"]
        writer = csv.DictWriter(after, fieldnames=fieldName)
        writer.writeheader()

        for data in rdr:
            i += 1


            if data['수집날짜'] == None:
                print(data)
                continue

            # if i < 165302:
            #     continue
            else:
                row = {}

                row["date"] = data['날짜'].replace('"', '')
                row["datetime"] = data['날짜시간'].replace('"', '')
                row["day"] = data['요일'].replace('"', '')
                row["ip"] = data['변화아이피'].replace('"', '')
                row["url"] = data['url'].replace('"', '')
                row["host"] = data['host'].replace('"', '')
                row["sWord"] = data['검색어원본'].replace('"', '')
                row["sWord_Spacing"] = data['검색어_띄어쓰기'].replace('"', '')
                writer.writerow(row)



    print(i)




#
# with open('D:\\portal.csv', encoding='utf-8-sig', newline='') as f:
#     rdr = csv.DictReader(f)
#     i = 0
#     ip = str()
#     for data in rdr:
#         ip = data['변화아이피']
#         if ip not in  result[keys.index(ip)].keys():
#             result[keys.index(ip)]['ip'] = ip
#         else:
#             print(ip + " not in keys")
#         da = OrderedDict()
#         da['date'] = data['날짜시간']
#         da['day'] = data['요일']
#         da['url'] = data['url']
#         da['host'] = data['host']
#         da['sWord'] = data['검색어원본']
#         da['sWordSpace'] = str(data['검색어_띄어쓰기']).split(' ')
#
#         result[keys.index(ip)]['search'].append(da)
#         i += 1
#         if i == 10000:
#             print(result)
#             with open('portal_Search2.json', 'w', encoding="utf-8") as make_file:
#                 json.dump(result, make_file, ensure_ascii=False, indent="\t")
#             break


