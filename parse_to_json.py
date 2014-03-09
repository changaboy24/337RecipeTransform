import json

def grading_json(recipe):
	"Given a 'recipe' dictionary returned from recipe_run.main(), returns a JSON file with specified structure."
	return json.dumps(recipe)