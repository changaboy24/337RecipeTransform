import database, recipe_parser

def getMethods(recipe_url):
	all_methods, all_tools = database.get_tools_and_methods()
	# feed in the url of the recipe
	content = recipe_parser.http_string(recipe_url)

	methods = []
	# tools = []

	#send it to directions to get the recipe's directions section
	recipDirections = recipe_parser.directions_steps(content)
	
	# to print each instruction
	# for direction in recipDirections:
	# 	found_tool = search(direction,all_tools)
	# 	if found_tool != None and found_tool not in tool:
	# 		tools.append(found_tool)

		found_method = search(direction, all_methods)
		if found_method != None and found_method not in method:
			methods.append(found_method)
			
	return methods#, tools


def search(direction, tools_or_methods):
	for token in direction.split():
		token = dePunc(direction.lower())

		if token in tools_or_methods:
			return token

def dePunc(rawword):
    """ remove punctuation in the input string """
    L = [ c for c in rawword if 'A' <= c <= 'Z' or 'a' <= c <= 'z' ]
    word = ''.join(L)
    return word