import pymongo, csv
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['db']
# categories = ["proteins","dairy","cooking-liquids","spices-sauces","vegetables","fruits","starches"]
categories = ["proteins"]

def categorize(ingredient_name):
	for category in categories:
		if db[category].find({"name":ingredient_name}).count() > 0:
			return category

def init_db_collection(collectionName):
	client = MongoClient('localhost', 27017)

	collection = db[collectionName]

	actualCollection = db[collectionName].remove() ##did this so it doesn't keep appending if you rerun it
	actualCollection = db[collectionName]

	return actualCollection

##collection name will be "category"
##imports from "category".txt
def import_category(category):
	attributes = ["name","vegetarian","healthy","east-asian","indian","spanish","american","italian","no-cuisine"]

	collection = init_db_collection(category)

	file_name = category+".csv"
	with open(file_name, "rb") as csv_file:
		rows = csv.reader(csv_file, delimiter=",")
		csv_file.readline()##skips first line

		for row in rows:
			ingredient = {}
			for attr, value in enumerate(row):
				ingredient[attributes[attr]] = value

			collection_id = collection.insert(ingredient)



			
def main():
	for category in categories:
		import_category(category)
main()
categorize("beef")
