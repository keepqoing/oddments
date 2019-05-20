import pymongo
from pymongo import MongoClient

conn = MongoClient('127.0.0.1')
db = conn.test

col = db.portal

# pipeline = list()
#
# pipeline.append({'$group' : {'_id' : '$address', 'price' : {'$push' : '$price'}}})
#
# data = col.aggregate(pipeline)

data = col.find()

for doc in data:
    print(doc)


mongo --quiet {test} --eval "printjson(db.zillow.find())" > D://output.json

mongo localhost:27017/test --eval "printjson(db.zillow.find())" >> D://output.json
