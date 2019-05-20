from apriori import Apriori

def getDataset():
    with open("명제석.txt", encoding="utf-8-sig") as f:
        keys = set()
        transactionData = list()
        for line in f:
            line = str(line).replace("\n", "")
            transactionItems = str(line).split(",")
            transactionData.append(transactionItems)

    return transactionData

# dataset = [
#     ['bread', 'milk'],
#     ['bread', 'diaper', 'beer', 'egg'],
#     ['milk', 'diaper', 'beer', 'cola'],
#     ['bread', 'milk', 'diaper', 'beer'],
#     ['bread', 'milk', 'diaper', 'cola'],
# ]

dataset = getDataset()

minsup = 0.01
minconf = 0.4

ap = Apriori(dataset, minsup, minconf)
# run algorithm
ap.run()
# print out frequent itemset
ap.print_frequent_itemset()
# print out rules
ap.print_rule()
