import pymongo, csv
from pymongo import MongoClient


"""This file imports a list of csv's and puts them into the database."""

############################################################################
#####Important Functions
############################################################################

#input: ingredient name (i.e. chicken, salt)
#output: category (i.e. protein, spice-sauce)
def categorize(ingredient_name):
	for category in food_categories:
		if db[category].find({"name":ingredient_name}).count() > 0:
			return category

#input: ingredient name (i.e. chicken, tofu)
#output: 1/0/"nothing found" (i.e. 0, 1)
#only looks through proteins.csv and cooking-liquids.csv
def is_vegetarian(ingredient_name):
	for category in ["proteins"]:#, cooking-liquids"]:
		if db[category].find({"name":ingredient_name}).count() > 0:
			return db[category].find_one({"name":ingredient_name})["vegetarian"]
	return "nothing found"

def to_vegetarian(ingredient_name):
	""

def to_meat(ingredient_name):
	""

def to_cuisine(cuisine, ingredient_name):
	""

def to_healthy(ingredient_name):
	""

def to_unhealthy(ingredient_name):
	""

def is_action_past_tense(action):
	""

def find_tool_for_action(action):
	""



############################################################################
####Backend Functions
############################################################################

client = MongoClient('localhost', 27017)
db = client['db']
# categories = ["proteins","dairy","cooking-liquids","spices-sauces","vegetables","fruits","starches"]
food_categories = ["proteins"]

#initializes a collection
def init_db_collection(collectionName):
	client = MongoClient('localhost', 27017)

	collection = db[collectionName]

	actualCollection = db[collectionName].remove() ##did this so it doesn't keep appending if you rerun it
	actualCollection = db[collectionName]

	return actualCollection

##collection name will be "category"
##imports from "category".txt
def import_foods():
	attributes = ["name","vegetarian","healthy","east-asian","indian","spanish","american","italian","no-cuisine"]
	for category in food_categories:
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
	import_foods()
main()
is_vegetarian("beef")
