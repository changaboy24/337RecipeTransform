from recipe_parser import *
from string import *
import urllib2
from bs4 import BeautifulSoup
import nltk


allrecipes = "http://allrecipes.com/Recipe/Classic-Cocktail-Meatballs/Detail.aspx?event8=1&prop24=SR_Thumb&e11=stove&e8=Quick%20Search&event10=1&e7=Recipe&soid=sr_results_p1i6"


page = urllib2.urlopen(allrecipes).read()
soup = BeautifulSoup(page)
name = str(soup.title)
start = 7
end = name.find('- Allrecipes.com', start)
title = name[start:end].lstrip().rstrip()

methods = ['saute', 'broil', 'boil', 'poach', 'bake', 'roast', 'grill', 'double boil',
'pan fry', 'sweat', 'torch', 'flambe', 'blanch', 'braise', 'scald', 'simmer', 
'steam', 'barbecue', 'fry', 'deep fry']

tools = ['saucepan', 'baking dish', 'casserole dish', 'oven', 'dutch oven', 'pot', 'stove', 'foil', 'skillet',
'pan', 'frying pan', 'slow cooker', 'grill', 'deep-fryer']


method = []
tool = []

def getDirections(recipe):
	# feed in the url of the recipe
	url = http_string(recipe)

	#send it to directions to get the recipe's directions section
	recipDir = directions_steps(url)
	
	x = []
	y = []
	# to print each instruction
	for i in range(0, len(recipDir)):

		# x will be the method retrieved from searchMethod
		line = str(recipDir[i]).split()
		x = searchMethod(line)
		y = searchTools(line)

		if x != None and x not in method:
			method.append(x)

		if y != None and y not in tool:
			tool.append(y)
			
	return method

def searchMethod(recipe):
	""" search the recipe for a cooking method,
	then return it to be added to the list """
	for w in recipe:
		x = w.lower()
		x = dePunc(x)

		if x in methods:
			return x
		else:
			continue


def searchTools(recipe):
	""" search the recipe for a cooking tools,
	then return it to be added to the list """
	for w in recipe:
		x = w.lower()
		x = dePunc(x)

		if x in tools:
			return x
		else:
			continue


def dePunc(rawword):
    """ remove punctuation in the input string """
    L = [ c for c in rawword if 'A' <= c <= 'Z' or 'a' <= c <= 'z' ]
    word = ''.join(L)
    return word