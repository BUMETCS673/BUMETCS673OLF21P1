from urllib.parse import urlencode
from flask import render_template, request, redirect, url_for, session
from config import app
from pantry import PantryManager
from favoriteRecipes import FavoriteRecipeManager
from spoon import searchRecipes, getRecipeDetail, getSimilarRecipeID
from authentication import auth0, AUTH0_AUDIENCE, AUTH0_CALLBACK_URL,\
    AUTH0_CLIENT_ID

# /route will show our index template
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
    allReq = request.args.get('searchType')
    usePantry = request.args.get('incPantry')
    # had to collect pantry ingredients here to avoid circular ref
    if (usePantry != None) and (session != {}):
        pm = PantryManager(session['profile']['user_id'])
        if ingredients != '':
            ingredients = ingredients + ',' + pm.getPantry()
        else:
            ingredients = pm.getPantry()
    print('ing: ' + ingredients)

    if ingredients == '':
        results = []
        return render_template('recipe.html', results=results)
    results = searchRecipes(ingredients, diet, intolerances, allReq)
    # set second argument to pass the data
    return render_template('recipe.html', results=results)


@app.route("/recipe/<recipe_id>")
def recipeDetail(recipe_id):
    data = getRecipeDetail(recipe_id)
    similarRecipeID = getSimilarRecipeID(recipe_id)
    return render_template('recipe_detail.html', recipe=data, similarRecipeID=similarRecipeID)

@app.route("/pantry")
def pantry():
    # set user and create Pantry Manager
    user = "TestUser"  # for testing purposes
    if session != {}:
        user = session['profile']['user_id']
    pm = PantryManager(user)

    # pantry ingredients to show
    pantryItems = pm.dispPantry()
    return render_template("pantry.html", items=pantryItems)


@app.route("/pantry/add", methods=['POST'])
def pantryAdd():

    # set user and create Pantry Manager
    user = "TestUser"  # for testing purposes
    if session != {}:
        user = session['profile']['user_id']
    pm = PantryManager(user)

    # handle added ingredients
    ingredients = request.form['ingredients']
    if ingredients != None:
        pm.addPantry(ingredients)

    ingredients = request.args.get('ingredients')
    return redirect(url_for('pantry'))

@app.route("/pantry/del/<id>", methods=['POST'])
def pantryDel(id):
    # set user and create Pantry Manager
    user = "TestUser"  # for testing purposes
    if session != {}:
        user = session['profile']['user_id']
    pm = PantryManager(user)
    pm.delPantryItem(id)
    return redirect(url_for('pantry'))


@app.route("/pantry/del_all/", methods=['POST'])
def pantryDelAll():
    # set user and create Pantry Manager
    user = "TestUser"  # for testing purposes
    if session != {}:
        user = session['profile']['user_id']
    pm = PantryManager(user)
    pm.delPantryUser()
    return redirect(url_for('pantry'))


# Here we're using the /callback route.
@app.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    # TODO - change this from name and picture to pantry and recipes
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    return redirect('/')

@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL,
                                    audience=AUTH0_AUDIENCE)

@app.route('/logout')
def logout():
    session.clear()
    params = {'returnTo': url_for('index', _external=True),
              'client_id': AUTH0_CLIENT_ID}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


@app.route('/favorite_recipes')
def getFavoriteRecipes():

    userID = "TestUser"  # for testing purposes
    if session != {}:
        userID = session['profile']['user_id']
    db = FavoriteRecipeManager(userID)
    favRecipes = db.getFavoriteRecipes()
    favRecipesList = favRecipes.split(", ")
    results = []
    # check for empty favorites list
    if (favRecipesList[0] != ''):
        for recipe in favRecipesList:
            print(recipe)
            results.append(getRecipeDetail(recipe))
    else:
        results = []
    return render_template('favorite_recipes.html', recipes=results)


@app.route('/recipe_detail/<recipe_id>')
def favoriteThisRecipe(recipe_id):

    userID = "TestUser"  # for testing purposes
    if session != {}:
        userID = session['profile']['user_id']
    # Take the given id and add it to the database
    db = FavoriteRecipeManager(userID)
    db.addFavoriteRecipe(recipe_id)

    # get the recipe again
    data = getRecipeDetail(recipe_id)
    similarRecipeID = getSimilarRecipeID(recipe_id)
    # now update the page to inform the user that they added the recipe to the database
    return render_template('recipe_detail.html', recipe=data, similarRecipeID=similarRecipeID, message=True)

@app.route('/remove_recipe/<recipe_id>')
def removeFromFavorites(recipe_id):

    userID = "TestUser"  # for testing purposes
    if session != {}:
        userID = session['profile']['user_id']
    # Take the given id and remove from database
    db = FavoriteRecipeManager(userID)
    db.delFavoriteRecipe(recipe_id)

    return getFavoriteRecipes()


