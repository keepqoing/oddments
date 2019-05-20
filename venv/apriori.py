# Importing dataset
import pandas as pd
dataset=pd.read_csv("Movie_Record.csv",header=None)

# Data Preprocessing
transactions=[]
for i in range(0,len(dataset)):
    transactions.append([str(dataset.values[i,j]) for j in range(0,20)])

# Training 
from apyori import apriori
rules=apriori(transactions,min_support=0.003,min_confidence=0.2,min_length=2,min_lift=3)    

# visualizing
results=list(rules)

for i in results:
    print(i)
# import matplotlib.pyplot as plt
# plt.itemFrequency(results)