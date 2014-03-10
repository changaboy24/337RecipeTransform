import database, recipe_parser
# from bs4 import BeautifulSoup


allrecipes = "http://allrecipes.com/Recipe/Classic-Cocktail-Meatballs/Detail.aspx?event8=1&prop24=SR_Thumb&e11=stove&e8=Quick%20Search&event10=1&e7=Recipe&soid=sr_results_p1i6"


# page = urllib2.urlopen(allrecipes).read()
# soup = BeautifulSoup(page)
# name = str(soup.title) recipe_parser.recipe_name(allrecipes)
# start = 7
# end = name.find('- Allrecipes.com', start)
# title = recipe_parser.recipe_name(allrecipes)

def getMethods(recipe_url):
	all_methods, all_tools = database.get_tools_and_methods()
	# feed in the url of the recipe
	content = recipe_parser.http_string(recipe_url)

	method = []

	#send it to directions to get the recipe's directions section
	recipDirections = recipe_parser.directions_steps(content)
	
	# to print each instruction
	for direction in recipDirections:
		# found_tool = search(direction,all_methods)
		# if found_tool != None and found_tool not in tool:
		# 	tool.append(found_tool)

		found_method = search(direction, all_tools)
		if found_method != None and found_method not in method:
			tool.append(found_tool)

	# for i in range(0, len(recipDirections)):
	# 	print i

	# 	# x will be the method retrieved from searchMethod
	# 	line = str(recipDirections[i]).split()
	# 	print line
	# 	x = searchMethod(line)
	# 	print x
	# 	y = searchTools(line)
	# 	print y

	# 	if x != None and x not in method:
	# 		method.append(x)

	# 	if y != None and y not in tool:
	# 		tool.append(y)
			
	return method

# def searchMethod(recipe):
# 	""" search the recipe for a cooking method,
# 	then return it to be added to the list """
# 	for w in recipe:
# 		x = w.lower()
# 		x = dePunc(x)

# 		if x in all_methods:
# 			return x
# 		else:
# 			continue

def search(direction, tools_or_methods):
	for token in direction.split():
		token = dePunc(direction.lower())

		if token in tools_or_methods:
			return token

# def searchTools(recipe):
# 	""" search the recipe for a cooking tools,
# 	then return it to be added to the list """
# 	for w in recipe:
# 		x = w.lower()
# 		x = dePunc(x)

# 		if x in all_tools:
# 			return x
# 		else:
# 			continue


def dePunc(rawword):
    """ remove punctuation in the input string """
    L = [ c for c in rawword if 'A' <= c <= 'Z' or 'a' <= c <= 'z' ]
    word = ''.join(L)
    return word
print getMethods("http://allrecipes.com/Recipe/Braised-Corned-Beef-Brisket/Detail.aspx?evt19=1")