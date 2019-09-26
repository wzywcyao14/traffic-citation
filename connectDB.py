#This module uses python to connect to MongoDB and create new database

import pymongo  # use python to interact with mongoDB database server

def dbCreation (dbname: str, colname: str): #return the collection of database

	# local cluster
	# connection = pymongo.MongoClient('localhost', 27017) # 27017 is the default port

    # M0 cluster in mongo Atlas
    # connection = pymongo.MongoClient("mongodb+srv://wyao:yao14@citation-bapzv.mongodb.net/test?retryWrites=true&w=majority")
	# M10 cluster in mongo Atlas
    # connection = pymongo.MongoClient("mongodb+srv://wyao:yao14@cluster0-ubllg.mongodb.net/test?retryWrites=true&w=majority")



    # create database
    database = connection[dbname]
    print(database)
	# create collection
    collection = database[colname]
    print (collection)

    return collection


