from flask import Flask, render_template, request
from spoon import searchRecipes

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
    intolerance = request.args.get('intolerance')
    hits = searchRecipes(ingredients, diet, intolerance)
    # set second argument to pass the data
    return render_template('recipe.html', hits=hits)

# test module import
if __name__ == "__main__":
    app.run(debug = True)