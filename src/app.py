import random

from flask import Flask, render_template, request
from spoon import searchRecipes
from flask_sqlalchemy import SQLAlchemy

# flask class instance

app = Flask(__name__)

# set up database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/spoon.db'
db = SQLAlchemy(app)


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingredientName = db.Column(db.String(80), nullable=False)
    ingredientQuantity = db.Column(db.String(120), nullable=False)
    expirationDate = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<Id: %r>' % self.id + '<Ingredient Name: %r>' % self.ingredientName \
               + '<Ingredient Quantity: %r>' % self.ingredientQuantity \
               + '<Expiration Date: %r>\n' % self.expirationDate


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


@app.route("/insertIngredient")
def insertIngredient():
    ingredient_dict = {'name': request.args.get('ingredientName'),
                       'quantity': request.args.get('ingredientQuantity'),
                       'expiration_date': request.args.get('expirationDate')}
    # save to database
    db.create_all()

    rand_int = random.randint(0, 999999999)
    ingredient_object = Ingredient(id=rand_int,
                                   ingredientName=ingredient_dict['name'],
                                   ingredientQuantity=ingredient_dict['quantity'],
                                   expirationDate=ingredient_dict['expiration_date'])

    db.session.add(ingredient_object)
    db.session.commit()

    print(Ingredient.query.all())  # DEBUG
    return render_template('submittedIngredient.html', results=ingredient_dict)


def clearData(db):
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table: %s' % table)
        db.session.execute(table.delete())
    db.session.commit()


if __name__ == "__main__":
    # test module import
    app.run(debug=True)
