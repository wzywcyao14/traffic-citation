import pymongo  # use python to interact with mongoDB database server
import connectDB
# import csv  # csv module to RD/WR csv data file
# import json

# # define names for database and collection
databaseName = 'citation'
collectionName = 'record'
# create a database in MongoDB
collection = connectDB.dbCreation(databaseName, collectionName)

import pandas as pd
import numpy as np
counter = 0
# break the input file into specfied chunks instead of loading the whole file into memory
df = pd.read_csv('Data/parking-citations.csv', chunksize=1000)
counter = 0
# print(df.get_chunk(4))
# print(type(df))

collection.remove()
for chunk in df:
    if counter == 5328:
        break
    else:
        # print(type(chunk))
        # print(chunk)
        collection.insert_many(chunk.to_dict('records'))
        # collection.insert_many(np.array(chunk))
        counter += 1
# for chunk in df:
#     collection.insert_many(chunk.to_dict('records'))

collection.create_index([("Fine amount",1),("Issue Date",1)])
collection.create_index([("Issue time",1),("Issue Date",1)])
collection.create_index([("Location",1),("Issue Date",1)])
collection.create_index([("Make",1),("Issue Date",1)])
collection.create_index([("Issue Date",1)])

