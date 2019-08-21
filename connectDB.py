#This module uses python to connect to MongoDB and create new database

import pymongo  # use python to interact with mongoDB database server

def dbCreation (dbname: str, colname: str): #return the collection of database

	# connect to mongoDB database
	connection = pymongo.MongoClient('localhost', 27017) # 27017 is the default port
	# create database
	database = connection[dbname]
	print(database)
	# create collection
	collection = database[colname]
	print (collection)

	return collection 


