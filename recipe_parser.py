import nltk, json, re, numpy, urllib2, fractions, database

def http_string(url):
	"Takes a url and returns a string of its contents."
	return urllib2.urlopen(url).read()

def find_ingredient(str,index):
	"Returns the starting index of an ingredient in the page."
	start = str.find('itemprop=\"ingredients',index)
	if start!=-1:
		start = start + 19
	return start
	
def ingredient_section(str,index):
	"Returns the section of the page that contains the next ingredient information."
	start = find_ingredient(str,index)
	end = str.find('</p>',start)
	return str[start:end]
	
def ingredient_amount(section):
	"Returns the amount of an ingredient in a section."
	start = section.find('ingredient-amount\">')
	start = start + 19
	end = section.find('</sp',start)
	return section[start:end]
	
def ingredient_name(section):
	"Returns the name of an ingredient in a section."
	start = section.find('ingredient-name\">')
	start = start + 17
	end = section.find('</sp',start)
	return section[start:end]

def amount_check(section):
	"Checks that the section contains ingredient amount information."
	if section.find('ingredient-amount\">') == -1:
		return False
	return True
	
def name_check(section):
	"Checks that the section contains ingredient name information."
	if section.find('ingredient-name\">') == -1:
		return False
	return True
	
def ingredients(str):
	"Returns a list of tuples of the ingredients split into amount and name."
	out =[]
	index = 0
	while index != -1:
		section = ingredient_section(str,index)
		amount = ingredient_amount(section)
		name = ingredient_name(section)
		if amount_check(section) and name_check(section):
			[quantity,measurement] = amount_split(amount)
			[name,descriptor,prep,category] = name_split(name)
			out.append((name,quantity,measurement,descriptor,prep,category))
		index = find_ingredient(str,index)
	return out

def directions_section(str):
	"Returns the section of the page containing the directions."
	start = str.find('class=\"directions')
	end = str.find('</ol>',start)
	return str[start:end]
	
def find_direction(section,index):
	"Returns the starting index of a direction in the page."
	start = section.find('erwrap break\">',index)
	if start!=-1:
		start = start + 14
	return start

def direction_string(section,index):
	"Returns the direction string in the section, starting the search at index."
	end = section.find('</sp',index)
	return section[index:end]
	
def directions(str):
	"Returns a list of the directions split by steps in page."
	out = []
	section = directions_section(str)
	index = find_direction(section,0)
	while index != -1:
		out.append(direction_string(section,index))
		index = find_direction(section,index)
	return out

def sentence_tokenize(str):
	"Uses NLTK sentence tokenizer to tokenize string into sentences."
	sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
	return sent_detector.tokenize(str)
	
def directions_steps(str):
	out = []
	for step in directions(str):
		out.extend(sentence_tokenize(step))
	return out
	
def amount_split(str):
	"Takes a string containing a quantity and a measurement, returning them as two elements in an array."
	tokens = nltk.word_tokenize(str)
	if len(tokens) == 1:
		measurement = ''
	elif len(tokens) == 2:
		measurement = tokens[1]
		tokens = [tokens[0]]
	elif tokens[-2] == ')':
		measurement = ''.join(tokens[-5:-3])+' '+''.join(tokens[-3:-1])+' '+tokens[-1]
		tokens = tokens[0:-5]
	elif tokens[-1] == ')':
		measurement = ''.join(tokens[-4:-2])+' '+''.join(tokens[-2::])
		tokens = tokens[0:-4]
	else:
		measurement = tokens[-1]
		tokens = tokens[0:-1]
	amount = 0
	for num in tokens:
		amount = amount + float(fractions.Fraction(num))
	if measurement!='' and measurement[-1] == 's' and measurement[-2]!='s':
		measurement = measurement[0:-1]
	return [amount,measurement]

def name_split(str):
	name = str
	prep = ''
	str = str.split(', ')
	if len(str) == 2:
		[name,prep]=str
	[descriptor,name,category] = name_category(name)
	return [name,descriptor,prep,category]

def name_category(str):
	tokens = str.split(" ")
	descriptor = []
	while len(tokens) != 0:
		category = database.categorize(' '.join(tokens))
		if category == 'notfound' and len(tokens) == 1:
			return ['',str,False]
		elif category == 'notfound':
			descriptor.append(tokens[0])
			tokens = tokens[1::]
		else:
			return [' '.join(descriptor),' '.join(tokens),category]

def recipe_name(url):
	"Returns recipe name from url string."
	start = url.find('ecipe/')+6
	url = url[start::]
	end= url.find('/')
	name = ' '.join(url[0:end].split('-'))
	return name

