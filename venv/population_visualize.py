import datetime
import time
from collections import OrderedDict

import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter
from pymongo import MongoClient


# Fault_Find_Cause1
# csv 파일을 읽어서 Transaction의 형태로 저장
def getDataset(country, item):
    # 리턴
    dataSet = []

    client = MongoClient('mongodb://127.0.0.1:27017')

    db = client.test
    collection = db.world_pop

    #aggregation pipeline
    pipeline = list()
    pipeline.append({'$match' : {"countryName" : country}})
    pipeline.append({'$unwind' : "$historical_Data"})
    pipeline.append({'$sort' : {"historical_Data.year" : 1}})
    result = collection.aggregate(pipeline)

    # Save historical data 
    for doc in result:
        # print(doc)
        sDate = datetime.datetime.strptime(doc['historical_Data']['year'], "%Y")
        value = float(doc['historical_Data'][item].replace(",", "").replace(" %",""))
        onedata = [sDate, value]
        dataSet.append(onedata)

    # aggregation pipeline  
    pipeline.clear()
    pipeline.append({'$match': {"countryName": country}})
    pipeline.append({'$unwind': "$forecast_Data"})
    pipeline.append({'$sort': {"forecast_Data.year": 1}})
    pipeline.append({'$project': {"forecast_Data": 1}})
    result = collection.aggregate(pipeline)
    
    # Save forecast data 
    for doc in result:
        # print(doc)
        sDate = datetime.datetime.strptime(doc['forecast_Data']['year'], "%Y")
        value = float(doc['forecast_Data'][item].replace(",","").replace(" %",""))
        onedata = [sDate, value]
        dataSet.append(onedata)

    return dataSet

def set_plot(ax, item):
    # ax.plot([1,2])
    ax.set_xlabel('dates')
    ax.set_ylabel(item)

    # Set in mongoData-axis every 10 years
    years = YearLocator(10)
    # Show only years
    yearsFmt = DateFormatter('%Y')

    # Format the ticks
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.autoscale_view()
    ax.fmt_xdata = DateFormatter('%Y')

    # Show grid
    ax.grid(True)




def draw(country, itemList):
    itemListlen = len(itemList)
    cols = 2
    rows = int(itemListlen/2)+ itemListlen%2
    lastrow = 0
    if itemListlen%2 == 1:
        lastrow = 1
    else:
        lastrow = cols

    print(rows, cols, lastrow )


    fig = plt.figure(figsize=(9, 16))
    plt.title(country)
    plt.tight_layout()

    axs = []

    index = 1
    for row in range(0,rows):
        for col in range(0,cols):
            ax = 0
            if index == itemListlen:
                if lastrow == 1:
                    ax = fig.add_subplot(rows, lastrow, rows)
                else:
                    ax = fig.add_subplot(rows, lastrow, index)

            elif index > itemListlen:
                break
            else:
                ax = fig.add_subplot(rows, cols, index)
            axs.append(ax)
            index += 1

    for i, item in enumerate(itemList):
        print(i, item, axs[i])
        mongoData = np.array(getDataset(country, item))

        axs[i].plot_date(mongoData[:, 0], mongoData[:, 1], "-")
        set_plot(axs[i], item)
        fig.autofmt_xdate()
        if item in ["globalRank"]:
            plt.gca().invert_yaxis()


    print(axs)


    plt.show()

itemList =  ['population', 'yearlyChangePer','yearlyChange', 'migrants', 'medianAge', 'fertilityRate', 'density', 'urbanPopPer', 'urbanPop', 'shareOfWorldPop' , 'worldPopulation', 'globalRank']

draw("South Korea", itemList)