import pymongo, csv, random
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
	return 'notfound'

#input: ingredient name (i.e. chicken, tofu)
#output: 1/0/"nothing found" (i.e. 0, 1)
#only looks through proteins.csv and cooking-liquids.csv
def is_vegetarian(ingredient_name):
	for category in ["proteins", "base liquids","solid fats"]:
		if db[category].find({"name":ingredient_name}).count() > 0:
			return db[category].find_one({"name":ingredient_name})["vegetarian"]
	return "notfound"

def to_vegetarian(ingredient_name):
	if categorize(ingredient_name) in ["proteins","base liquids","solid fats"]:
		if is_vegetarian(ingredient_name):
			return ingredient_name
		else:
			return find_replacement(ingredient_name, "vegetarian",1)
	return ingredient_name

def to_meat(ingredient_name):
	if categorize(ingredient_name) in ["proteins","base liquids","solid fats"]:
		return find_replacement(ingredient_name, "vegetarian","")
	return ingredient_name

def to_cuisine(cuisine, ingredient_name):
	return find_replacement(ingredient_name, cuisine,1)

def to_healthy(ingredient_name):
	return find_replacement(ingredient_name, "healthy",1)

def to_unhealthy(ingredient_name):
	return find_replacement(ingredient_name, "healthy","")

def is_action_past_tense(action):
	if db.actions.find({"past-tense":action}).count() > 0:
		return True
	return False

def find_prep_tool_for_action(action):
	for attr in ["food-prep", "past-tense"]:
		if db.actions.find({attr:action}).count() > 0:
			return db.actions.find_one({attr:action})["tool"]
	return "notfound"

def find_action_for_tool(tool):
	if db.actions.find({"tool":tool}).count() > 0:
		return db.actions.find_one({"tool":tool})["food-prep"]
	return "notfound"

def find_method_from_tool(tool):
	if db["cooking-tools"].find({"tool":tool}).count() > 0:
		return db["cooking-tools"].find_one({"tool":tool})["method"]
	return "notfound"
	
def detect_tools(directions):
	tool_array = []
	all_tools = []
	all_actions = []
	collections = ["actions","prep-tools","cooking-tools"]
	for collection in collections:
		for row in db[collection].find():
			if len(row["tool"])> 0:
				all_tools.append(row["tool"].lower())	
			if collection == "actions":
				all_actions.append(row["food-prep"])
			
	for tool in all_tools:
		for direction in directions:
			if tool in direction and tool not in tool_array:
				tool_array.append(tool)
	
	for action in all_actions:
		for direction in directions:
			tool = find_prep_tool_for_action(action)
			if action in direction and tool not in tool_array and len(tool)>0:
				tool_array.append(find_prep_tool_for_action(action))
	return tool_array

def get_tools_and_methods():
	methods = []
	tools = []

	for row in db["cooking-tools"].find():
		methods.append(row["method"])
		tools.append(row["tool"])
	return methods, tools

############################################################################
####Back-end Functions
############################################################################

client = MongoClient('localhost', 27017)
db = client['db']
food_categories = ["proteins","cream","cheese","juice","alcohol","base liquids","solid fats","oils","bread","grain","seeds","pasta","rice","spices","sauces","vegetables","fruits","thickener"]

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
		put_into_db(category,attributes)

def import_actions():
	attributes = ["food-prep","past-tense","tool"]
	put_into_db("actions",attributes)

def import_prep_tools():
	attributes = ["tool","alt-names","bleh"]
	put_into_db("prep-tools",attributes)

def import_cooking_tools():
	attributes = ["tool","method","keywords"]
	put_into_db("cooking-tools",attributes)

def put_into_db(csv_name, attributes):
	collection = init_db_collection(csv_name)
	with open("csv/"+csv_name+".csv","rb") as csv_file:
			rows = csv.reader(csv_file, delimiter=",")
			csv_file.readline()##skips first line
			for row in rows:
				db_row = {}
				for attr, value in enumerate(row):
					db_row[attributes[attr]] = value
				collection_id = collection.insert(db_row)

def find_replacement(ingredient_name, transform, value):
	category = categorize(ingredient_name)
	value = str(value).lower()
	if fits_transform(ingredient_name,transform,value,category):
		return ingredient_name
	count = db[category].find({transform:value}).count()
	random_num = random.randint(0,count)
	if count > 0:
		try:
			return db[category].find({transform:value}).limit(-1).skip(random_num).next()['name']
		except:
			return ingredient_name
	return ingredient_name

def fits_transform(ingredient_name,transform,value,category):
	if db[category].find({"name":ingredient_name}).count() > 0:
		return value == db[category].find_one({"name":ingredient_name})[transform]
	else:
		return True
		
def main():
	import_foods()
	import_actions()
	import_prep_tools()
	import_cooking_tools()

main()
