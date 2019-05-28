import datetime
from collections import OrderedDict

import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter
from pymongo import MongoClient

# The function that loads data for a specific item and dates in a specific country in MongoDB
def getDataset(country, item):
    dataSet = []

    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.test
    collection = db.world_pop

    # Aggregation pipeline
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
        sDate = datetime.datetime.strptime(doc['forecast_Data']['year'], "%Y")
        value = float(doc['forecast_Data'][item].replace(",","").replace(" %",""))
        onedata = [sDate, value]
        dataSet.append(onedata)

    return dataSet


def set_plot(ax, item):
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


# The function to visualize data using matplotlib
def draw(countryList, itemList):
    # Set the size of the entire graph
    fig = plt.figure(figsize=(16, 9))
    plt.title(countryList)

    # Calculate the number of rows and columns needed to draw multiple graphs on one screen
    itemListlen = len(itemList)
    cols = 2
    rows = int(itemListlen/2)+ itemListlen%2
    lastrow = 0
    if itemListlen%2 == 1:
        lastrow = 1
    else:
        lastrow = cols

    if isinstance(itemList, list) == False:
        rows = 1
        cols = 1
        lastrow = 1

    # Create a subplot for each item and specify its location
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

    lineList = []

    if isinstance(itemList,list):
        # For each subplot, visualize the data loaded from mongoDB.
        for i, item in enumerate(itemList):
            print(i, item, axs[i])
            print(isinstance(countryList, list))

            # if countryList parameter is list type
            # draw multiple line graph
            if (isinstance(countryList, list)):
                for country in countryList:
                    mongoData = np.array(getDataset(country, item))
                    line = axs[i].plot_date(mongoData[:, 0], mongoData[:, 1], "-")
                    lineList.append(line[0])

            else:
                mongoData = np.array(getDataset(countryList, item))
                line = axs[i].plot_date(mongoData[:, 0], mongoData[:, 1], "-")
                lineList = [line[0]]

            set_plot(axs[i], item)
            fig.autofmt_xdate()

            if i == len(itemList) - 1:
                if (isinstance(countryList, list) == False):
                    countryList = [countryList]

                fig.legend(lineList,  # The line objects
                           labels=countryList,  # The labels for each line
                           loc="upper right",  # Position of legend
                           borderaxespad=1,  # Small spacing around legend box
                           title="Country"  # Title for the legend
                           )
            # Exception handling : reverse the y axis
            if item in ["globalRank"]:
                plt.gca().invert_yaxis()

    else:
        if (isinstance(countryList, list)):
            for country in countryList:
                mongoData = np.array(getDataset(country, itemList))
                line = axs[0].plot_date(mongoData[:, 0], mongoData[:, 1], "-")
                lineList.append(line[0])

        else:
            mongoData = np.array(getDataset(countryList, itemList))
            line = axs[0].plot_date(mongoData[:, 0], mongoData[:, 1], "-")
            lineList = [line[0]]

        set_plot(axs[0], itemList)
        # fig.autofmt_xdate()

        if (isinstance(countryList, list) == False):
            countryList = [countryList]
        fig.legend([lineList],  # The line objects
                   labels=countryList,  # The labels for each line
                   loc="upper right",  # Position of legend
                   borderaxespad=1,  # Small spacing around legend box
                   title="Country"  # Title for the legend
                   )

        # Exception handling : reverse the y axis
        if lineList in ["globalRank"]:
            plt.gca().invert_yaxis()
    plt.tight_layout()

    plt.show()

# The item list that can be selected
# ['population', 'yearlyChangePer','yearlyChange', 'migrants', 'medianAge', 'fertilityRate', 'density', 'urbanPopPer', 'urbanPop', 'shareOfWorldPop' , 'worldPopulation', 'globalRank']
# itemList =  ['population', 'yearlyChangePer','yearlyChange', 'migrants', 'medianAge', 'fertilityRate', 'globalRank']
itemList =  ['medianAge', 'fertilityRate', 'density', 'urbanPopPer', 'urbanPop', 'shareOfWorldPop' , 'worldPopulation', 'globalRank']


# only one country's data and only one item
draw("South Korea", "population")

# multiple country's data and only one item
draw(["South Korea","North Korea"], "yearlyChangePer")

# only one country's data and multiple item
draw("United States", ["urbanPop","urbanPopPer", "population"])

# multiple country's data and multiple item
draw(["United States", "Canada","South Korea"], ['medianAge', 'fertilityRate', 'density', 'urbanPopPer', 'urbanPop', 'shareOfWorldPop'])