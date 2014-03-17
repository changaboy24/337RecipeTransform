import json

def grading_json(recipe):
	"Given a 'recipe' dictionary returned from recipe_run.make_recipe_dict('url'), returns a JSON file with specified structure."
	recipe.pop('name',0)
	recipe.pop('intermediate methods',0)
	recipe.pop('directions',0)
	for ingredient in recipe['ingredients']:
		ingredient.pop('category',0)
	return json.dumps(recipe)