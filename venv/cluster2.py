from collections import OrderedDict
from collections import OrderedDict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from pymongo import MongoClient
from sklearn.cluster import KMeans


def getDataset():
    client = MongoClient('mongodb://127.0.0.1:27017')

    db = client.test
    collection = db.jane

    result = collection.find({},{"0.85":1, "17.45" :1, "2":1})
    x = []
    y = []

    for data in result:
        print(data)
        oneData = []
        oneData.append(float(data['fixed acidity']))
        oneData.append(float(data['volatile acidity']))
        # print(oneData)
        x.append(oneData)
        y.append(int(data['quality']))

    df = pd.DataFrame([attr1,attr2,attr3,attr4,attr5,attr6,attr7,attr8,attr9,attr10]).T
    corr = df.corr(method='pearson')
    print(corr)

    return x, y


x, y = getDataset()

X = np.array(x)

kmeans = KMeans(n_clusters=6)
kmeans.fit(X)


# plt.scatter(X[:, 0], X[:, 1], c=kmeans.labels_, cmap='rainbow')
# plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], color='black')
#
# plt.show()

plt.scatter(X[:, 0], X[:, 1], c=y, cmap='rainbow')

plt.show()

#
# with open('redwine.csv', encoding='utf-8-sig', newline='') as f1:
#     rdr = csv.DictReader(f1)
#     x = []
#     y = []
#
#     attr1 = []
#     attr2 = []
#     attr3 = []
#     attr4 = []
#     attr5 = []
#     attr6 = []
#     attr7 = []
#     attr8 = []
#     attr9 = []
#     attr10 = []
#
#     for data in rdr:
#         oneData = []
#         oneData.append(float(data['fixed acidity']))
#         # attr1.append(float(data['fixed acidity']))
#         # oneData.append(float(data['volatile acidity']))
#         # attr2.append(float(data['volatile acidity']))
#         # oneData.append(float(data['citric acid']))
#         # attr3.append(float(data['citric acid']))
#         # oneData.append(float(data['residual sugar']))
#         # attr4.append(float(data['residual sugar']))
#         # oneData.append(float(data['chlorides']))
#         # attr5.append(float(data['chlorides']))
#         # oneData.append(float(data['density']))
#         # attr6.append(float(data['density']))
#         # oneData.append(float(data['pH']))
#         # attr7.append(float(data['pH']))
#         # oneData.append(float(data['sulphates']))
#         # attr8.append(float(data['sulphates']))
#         oneData.append(float(data['alcohol']))
#         # attr9.append(float(data['alcohol']))
#
#         # oneData.append(float(data['quality']))
#         # attr10.append(float(data['quality']))
#         # print(oneData)
#         x.append(oneData)
#         y.append(int(data['quality']))
#     #
#     # df = pd.DataFrame([attr1,attr2,attr3,attr4,attr5,attr6,attr7,attr8,attr9,attr10]).T
#     # corr = df.corr(method='pearson')
#     # print(corr)
#     #
#     # for cor in corr:
#     #     print(corr[cor])
#
#
#     X = np.array(x)
#
#     kmeans = KMeans(n_clusters=6)
#     kmeans.fit(X)
#
#     for i, val in enumerate(kmeans.labels_):
#         print(val+1, y[i])
#
#
#     plt.scatter(X[:, 0], X[:, 1], c=kmeans.labels_, cmap='rainbow')
#     plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], color='black')
#
#     plt.show()
