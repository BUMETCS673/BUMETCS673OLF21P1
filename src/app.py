import requests
from flask import Flask, render_template, request
from spoon import searchRecipes
from dotenv import find_dotenv, load_dotenv
from os import environ as env

# flask class instance
app = Flask(__name__)

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
SPOON_API_KEY = env.get("SPOON_KEY")


# / route will show our index template
@app.route("/")
def index():
    return render_template("index.html")

# /about will show about page
app.route("/about")
def about():
    return render_template("about.html")

@app.route("/recipe")
def showRecipes():
    ingredients = request.args.get('ingredients')
    diet = request.args.get('diet')
    intolerances = request.args.get('intolerances')
    results = searchRecipes(ingredients, diet, intolerances)
    # set second argument to pass the data
    return render_template('recipe.html', results=results)


@app.route("/recipe/<recipe_id>")
def getRecipeDetail(recipe_id):
    req = f'https://api.spoonacular.com/recipes/{recipe_id}/information?&apiKey={API_KEY}'
    res = requests.get(req)
    data = res.json()
    return render_template('recipe_detail.html', recipe=data)

# test module import
if __name__ == "__main__":
    app.run(debug = True)