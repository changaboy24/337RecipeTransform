import recipe_parser, database, recipe_methods, pprint
from termcolor import colored

#model of recipe dictionary
#
#recipe ={	
#				"ingredients":	[{	
#												"name":	"",	
#												"quantity":	"",	
#												"measurement":	"",	
#												"descriptor":	"",	
#												"preparation":	"",
#												"category": ""
#								}
#				],	
#				"cooking method":	"",	
#				"cooking tools":	[],	
#				"name": "",
#				"directions": [],
#				"intermediate methods": ""
#}
recipe = {'ingredients':[]}
transform_codes = { 
	'v':'Vegetarian',
	'nv':'Non-Vegetarian',
	'h':'Healthier',
	'lh':'Less Healthy',
	'a':'American',
	'e':'East-Asian',
	's':'Spanish',
	'in':'Indian',
	'it':'Italian'}

def ingredient_display(ingredient):
	out = ['{0:.2f}'.format(ingredient['quantity'])]
	if out[0][-3::]=='.00':
		out[0] = out[0][0:-3]
	elif out[0][-3::]=='.25':
		if out[0][0]=='0':
			out[0] = '1/4'
		else:
			out[0] = out[0][0:-3]+' 1/4'
	elif out[0][-3::]=='.33':
		if out[0][0]=='0':
			out[0] = '1/3'
		else:
			out[0] = out[0][0:-3]+' 1/3'
	elif out[0][-3::]=='.50':
		if out[0][0]=='0':
			out[0] = '1/2'
		else:
			out[0] = out[0][0:-3]+' 1/2'
	elif out[0][-3::]=='.67':
		if out[0][0]=='0':
			out[0] = '2/3'
		else:
			out[0] = out[0][0:-3]+' 2/3'
	elif out[0][-3::]=='.75':
		if out[0][0]=='0':
			out[0] = '3/4'
		else:
			out[0] = out[0][0:-3]+' 3/4'
	if ingredient['measurement'] != '' and ingredient['quantity']>1:
		out.append(ingredient['measurement']+'s')
	elif ingredient['measurement']!= '':
		out.append(ingredient['measurement'])
	if ingredient['descriptor'] != '':
		out.append(ingredient['descriptor'])
	out.append(ingredient['name'])
	if ingredient['preparation'] != '':
		out.append('-')
		out.append(ingredient['preparation'])
	return out

def make_recipe_dict(url):
	recipe = {'ingredients':[],'cooking tools':[]}
	contents = recipe_parser.http_string(url)
	recipe['name'] = recipe_parser.recipe_name(url)
	recipe['directions'] = recipe_parser.directions(contents)


	ingredients = recipe_parser.ingredients(contents)
	for ingredient in ingredients:
		[iname,quantity,measure,descriptor,prep,category] = ingredient
		recipe['ingredients'].append({'name':iname.lower(),'quantity':quantity,'measurement':measure,'descriptor':descriptor,'preparation':prep, 'category':category})
		
		#find all tools implied by prep fields, add to 'cooking tools', (TODO:)and maybe add actions to 'intermediate methods'
		tool = database.find_prep_tool_for_action(prep)
		if tool != 'notfound' and tool not in recipe['cooking tools']:
			recipe['cooking tools'].append(tool)
	
	#find all tools implied by actions in directions, adding where appropriate
	#find all tools mentioned in directions, add to 'cooking tools', and maybe add actions to 'intermediate methods'
	recipe['cooking tools'].extend(database.detect_tools(recipe['directions']))
	#make 'cooking tools' a set
	recipe['cooking tools']= list(set(recipe['cooking tools']))
	#find cooking method and add to 'cooking method'
	#start with the directions and then move on to the tools if still not found
	methods = recipe_methods.getMethods(url)
	if methods ==[]:
		for tool in recipe['cooking tools']:
			method = database.find_method_from_tool(tool)
			if method != 'notfound':
				recipe['cooking method'] = method
	else:
		#grab last one because it is most likely to be the main cooking method
		recipe['cooking method'] = methods[-1]
	return recipe

def print_recipe(recipe):
	title_color = "green"
	print 
	print colored(recipe['name'],title_color)
	print '-----------------------'
	print
	print colored('Ingredients',title_color)
	print '------------'
	for ingredient in recipe['ingredients']:
		out = ingredient_display(ingredient)
		print ' '.join(out)
	print
	print colored('Directions',title_color)
	print '------------'
	for (num,step) in enumerate(recipe['directions']):
		print '{}. {:<30}'.format(str(num+1),step)
		print

def print_transform_prompt():
	#print table of transforms and codes
	print
	print '{:<18} {:<18}'.format('Transform','Code')
	print '{:<18} {:<18}'.format('------------','------------')
	for code in sorted(transform_codes.keys()):
		print '{:<18} {:<18}'.format(transform_codes[code],code)
	print

def transform_recipe(recipe, transform):
	replacement_names = {}
	for ingredient in recipe["ingredients"]:
		if ingredient["category"] != False:
			original_name = ingredient["name"]
			if transform=="v":
				ingredient["name"]=database.to_vegetarian(ingredient["name"])
			elif transform=="nv":
				ingredient["name"]=database.to_meat(ingredient["name"])
			elif transform=="h":
				ingredient["name"]=database.to_healthy(ingredient["name"])
			elif transform=="lh":
				ingredient["name"]=database.to_unhealthy(ingredient["name"])
			elif transform=="a":
				ingredient["name"]=database.to_cuisine("american",ingredient["name"])
			elif transform=="e":
				ingredient["name"]=database.to_cuisine("east-asian",ingredient["name"])
			elif transform=="s":
				ingredient["name"]=database.to_cuisine("spanish",ingredient["name"])
			elif transform=="in":
				ingredient["name"]=database.to_cuisine("indian",ingredient["name"])
			elif transform=="it":
				ingredient["name"]=database.to_cuisine("italian",ingredient["name"])

			##if there was a change, color the text red
			if ingredient["name"] != original_name:
				ingredient["name"] = colored(ingredient["name"],"red")
				ingredient["descriptor"] = ''
			replacement_names[original_name] = ingredient["name"]

	ordering = []
	for ingredient in replacement_names.keys():
		length = len(ingredient.split(' '))
		ordering.append([length,ingredient])
	ordering = sorted(ordering,reverse=True)
	#from longest ingredient name to shortest, replace the name with the new ingredient in each direction step
	for [num, ingredient] in ordering:
		for (count,step) in enumerate(recipe['directions']):
			recipe['directions'][count] = step.replace(ingredient,replacement_names[ingredient])

	return recipe

def pretty_print_dict(dictionary):
	pprint.PrettyPrinter(indent=4).pprint(dictionary)

def main ():
	url = raw_input('Enter URL to an AllRecipes recipe: ')
	recipe = make_recipe_dict(url)
	print_recipe(recipe)
	print_transform_prompt()

	transform = raw_input('How would you like to change ' + recipe["name"] + ' (enter code): ')
	recipe = transform_recipe(recipe, transform)

	recipe["name"] = transform_codes[transform] + " "+ recipe["name"]
	print_recipe(recipe)

	# pretty_print_dict(recipe)
#main()