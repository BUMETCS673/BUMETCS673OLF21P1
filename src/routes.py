from flask import render_template, request, redirect, url_for

from config import app
from pantry import PantryManager
from spoon import searchRecipes, getRecipeDetail


# / route will show our index template
@app.route("/")
def index():
    return render_template("index.html")


# /about will show about page
@app.route("/about")
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
def recipeDetail(recipe_id):
    data = getRecipeDetail(recipe_id)
    return render_template('recipe_detail.html', recipe=data)


@app.route("/pantry")
def pantry():
    # set user and create Pantry Manager
    user = "Tim"  # for testing purposes
    pm = PantryManager(user)

    # handle if ingredients are added
    ingredients = request.args.get('ingredients')
    if ingredients != None:
        pm.addPantry(ingredients)

    # pantry ingredients to show
    pantryItems = pm.dispPantry()
    return render_template("pantry.html", items=pantryItems)


# @app.route("/pantry/add", methods = ['POST'])
# def pantry_add():
#         # set user and create Pantry Manager
#     user = "Tim"    # for testing purposes
#     pm = PantryManager(user)
#     ingredients = request.args.get('ingredients')
#     print("ing: " + ingredients)
#     if ingredients != None:
#         pm.addPantry(ingredients)

#     return redirect(url_for('pantry'))


@app.route("/pantry/del/<id>", methods=['POST'])
def pantryDel(id):
    # set user and create Pantry Manager
    user = "Tim"  # for testing purposes
    pm = PantryManager(user)
    pm.delPantryItem(id)
    return redirect(url_for('pantry'))


@app.route("/pantry/del_all/", methods=['POST'])
def pantryDelAll():
    # set user and create Pantry Manager
    user = "Tim"  # for testing purposes
    pm = PantryManager(user)
    pm.delPantryUser()
    return redirect(url_for('pantry'))
