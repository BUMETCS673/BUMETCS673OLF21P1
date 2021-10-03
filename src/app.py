import requests
from flask import Flask, render_template, request
from spoon import searchRecipes, get_recipe_by_id

# flask class instance
app = Flask(__name__)

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
    data = get_recipe_by_id(recipe_id)
    return render_template('recipe_detail.html', recipe=data)

# test module import
if __name__ == "__main__":
    app.run(debug = True)