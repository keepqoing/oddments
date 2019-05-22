import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

X = np.array([[1,1],
              [1.5,2],
              [3,4],
              [5,7],
              [3.5,5],
              [4.5,5],
              [3.5,4.5] ])

plt.scatter(X[:, 0], X[:, 1], label='True Position')

plt.show()

print("----------")

import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

X = np.array([[1,1],
              [1.5,2],
              [3,4],
              [5,7],
              [3.5,5],
              [4.5,5],
              [3.5,4.5]
              ])

kmeans = KMeans(n_clusters=3)
kmeans.fit(X)

print(kmeans.cluster_centers_)
print(kmeans.labels_)

plt.scatter(X[:, 0], X[:, 1], label='True Position')

plt.show()

print("----------")

import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

X = np.array([[1,1],
              [1.5,2],
              [3,4],
              [5,7],
              [3.5,5],
              [4.5,5],
              [3.5,4.5] ])

kmeans = KMeans(n_clusters=3)
kmeans.fit(X)

print(kmeans.cluster_centers_)
print(kmeans.labels_)

plt.scatter(X[:, 0], X[:, 1], c=kmeans.labels_, cmap='rainbow')
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], color='black')

plt.show()
