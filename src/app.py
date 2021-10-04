import requests
from flask import Flask, render_template, request
from spoon import searchRecipes

# flask class instance
app = Flask(__name__)

API_KEY = '9e749e7df97047c38000f0f4addb64f9'

# / route will show our index template
@app.route("/")
def index():
    # The following is a placeholder for creating a user's favorite recipes
    req = f'https://api.spoonacular.com/recipes/complexSearch?query=Korean&number=3&apiKey={API_KEY}'
    res = requests.get(req)
    data = res.json()
    results = data['results']
    return render_template("index.html", results=results)

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


@app.route("/recipe_detail/<recipe_id>")
def getSmartRecipeRecommendation(recipe_id):
    data = getRecipeDetail(recipe_id)
    print(data)
    data = data[0]
    new_id = data['id']
    req2 = f'https://api.spoonacular.com/recipes/{new_id}/information?&apiKey={API_KEY}'
    res2 = requests.get(req2)
    data2 = res2.json()
    return render_template('recipe_detail.html', recipe=data2)


# test module import
if __name__ == "__main__":
    app.run(debug = True)