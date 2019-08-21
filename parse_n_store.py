import pymongo # use python to interact with mongoDB database server
import csv # csv module to RD/WR csv data file
import connectDB # connect to MongoDB server and create database

# define names for database and collection 
databaseName = 'newDB2'
collectionName = 'newCol2'

# create a database in MongoDB
collection = connectDB.dbCreation(databaseName,collectionName)


# load and parse the citation data (csv format)
with open('Data/parking-citations.csv' ,'r') as csv_file:
	csv_reader = csv.DictReader(csv_file)

	counter = 0
	# # store the parsed data into the created collection
	# for line in csv_reader:
	# 	collection.insert_one(line)
	# 	counter += 1 # count the number of documents


	#Test a limited number of data entry 
	for line in csv_reader:
		if counter == 4:
			break
		else:
			collection.insert_one(line)
			counter += 1

# Read operation
doc_1 = collection.find({'Ticket number': "4358765025"})
for row in doc_1:
	print(row)