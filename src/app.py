import requests
from flask import Flask, render_template, request, jsonify, _request_ctx_stack
from spoon import searchRecipes
import json
from six.moves.urllib.request import urlopen
from functools import wraps
from flask_cors import cross_origin
from jose import jwt


# flask class instance
app = Flask(__name__)

API_KEY = '9e749e7df97047c38000f0f4addb64f9'

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