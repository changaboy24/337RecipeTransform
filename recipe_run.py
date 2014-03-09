import recipe_parser

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
	'm':'Mexican',
	'in':'Indian',
	'it':'Italian'}

def ingredient_display(ingredient):
	out = [str(ingredient['quantity'])]
	if ingredient['measurement'] != '':
		out.append(ingredient['measurement'])
	if ingredient['descriptor'] != '':
		out.append(ingredient['descriptor'])
	out.append(ingredient['name'])
	if ingredient['preparation'] != '':
		out.append('-')
		out.append(ingredient['preparation'])
	return out
	
def main ():
	url = input('Enter URL to an AllRecipes recipe: ')
	recipename = recipe_parser.recipe_name(url)
	contents = recipe_parser.http_string(url)
	recipe['name'] = recipename
	recipe['directions'] = recipe_parser.directions(contents)
	ingredients = recipe_parser.ingredients(contents)
	for ingredient in ingredients:
		[iname,quantity,measure,descriptor,prep,category] = ingredient
		recipe['ingredients'].append({'name':iname,'quantity':quantity,'measurement':measure,'descriptor':descriptor,'preparation':prep, 'category':category})
	#find cooking method and add to 'cooking method'
	#find all tools implied by prep fields, add to 'cooking tools', and maybe add actions to 'intermediate methods'
	#find all tools implied by actions in directions, adding where appropriate
	#find all tools mentioned in directions, add to 'cooking tools', and maybe add actions to 'intermediate methods'
	#make 'cooking tools' a set
	#print table of transforms and codes
	print
	print '{:<18} {:<18}'.format('Transform','Code')
	print '{:<18} {:<18}'.format('------------','------------')
	for code in sorted(transform_codes.keys()):
		print '{:<18} {:<18}'.format(transform_codes[code],code)
	prompt = 'How would you like to change ' + recipename + ' (enter code): '
	transform = input(prompt)
	#for each ingredient check if it fits transform, if not substitute and update 'name' in 'ingredients'
		#also then update directions to reflect substitution, might need to order by longest name to avoid bad subs
	print transform_codes[code] + ' ' + recipename
	print
	print 'Ingredients'
	for ingredient in recipe['ingredients']:
		out = ingredient_display(ingredient)
		print ' '.join(out)
	print
	print 'Directions'
	for step in recipe['directions']:
		print '{:<30}'.format(step)