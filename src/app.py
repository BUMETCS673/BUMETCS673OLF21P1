from flask import Flask, render_template, request
from spoon import searchRecipes
from findSpecificRecipe import searchForRecipe

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
    print("ran wrong function")
    # set second argument to pass the data
    return render_template('recipe.html', results=results)

@app.route("/getRecipeByName")
def getRecipeByName():
    recipe_name = request.args.get('recipeName')
    recipe_results = searchForRecipe(recipe_name)

    return render_template('recipe.html', results=recipe_results)


# test module import
if __name__ == "__main__":
    app.run(debug=True)
