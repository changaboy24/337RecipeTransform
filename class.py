import recipe_parser

class Recipe:
	def __init__(self, url):
		self.name = ""
		self.ingredients = ""
		self.tools = []


	class Ingredient:
		def __init__(self, url):
			self.name = ""
			self.quantity = ""
			self.measurement = ""
			self.descriptor = ""
			self.preparation= ""

	class Methods:
		def __init__(self, url):
			self.primary_method = ""
			self.other_methods = []