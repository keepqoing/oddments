import time
from collections import OrderedDict

from pymongo import MongoClient
import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter
import datetime
import numpy as np
import pandas as pd

# Fault_Find_Cause1
# csv 파일을 읽어서 Transaction의 형태로 저장
def getDataset():
    client = MongoClient('mongodb://127.0.0.1:27017')

    db = client.test
    collection = db.portal4

    pipeline = list()

    pipeline.append({'$unwind': '$search'})
    pipeline.append({'$match' : {"search.sWord_Spacing" : "삼성"}})
    pipeline.append({'$group': {'_id': '$date', 'count': {'$sum': 1}}})
    pipeline.append({'$sort': {'_id' : 1}})


    result = collection.aggregate(pipeline, allowDiskUse=True)

    financeData = list()

    dates = []
    values = []

    for doc in result:
        sDate = datetime.datetime.strptime(doc['_id'], "%Y-%m-%d %H:%M:%S")
        # sDate = tmp.date()
        count = doc['count']
        # onedata = [sDate, count]
        # print(onedata)
        dates.append(sDate)
        values.append(count)
        # financeData.append(onedata)

    return dates,values

dates, values = getDataset()

date1 = dates[0]
date2 = dates[len(dates)-1]

years = YearLocator()   # every year
months = MonthLocator()  # every month
yearsFmt = DateFormatter('%Y')

fig, ax = plt.subplots()
ax.plot_date(dates, values, '-')

# format the ticks
ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(yearsFmt)
ax.xaxis.set_minor_locator(months)
ax.autoscale_view()

# format the coords message box
def price(x):
    return '$%1.2f' % x

ax.fmt_xdata = DateFormatter('%Y-%m-%d')
ax.fmt_ydata = price
ax.grid(True)

fig.autofmt_xdate()
plt.show()