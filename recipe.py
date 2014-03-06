import nltk, json, re, numpy, urllib2

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
			out.append((amount,name))
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
		
		