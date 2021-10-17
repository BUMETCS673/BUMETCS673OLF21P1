from urllib.parse import urlencode
from flask import render_template, request, redirect, url_for, session
from config import app
from pantry import PantryManager
from favoriteRecipes import FavoriteRecipeManager
from spoon import searchRecipes, getRecipeDetail, getSimilarRecipeID
from authentication import auth0, AUTH0_AUDIENCE, AUTH0_CALLBACK_URL,\
    AUTH0_CLIENT_ID, requires_auth
import ast

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
        results = ['blank']
        return render_template('recipe.html', results=results)
    results = searchRecipes(ingredients, diet, intolerances, allReq)
    # set second argument to pass the data
    return render_template('recipe.html', results=results)


@app.route("/recipe/<recipe_id>")
def recipeDetail(recipe_id):
    # fav flag
    recId = ''
    if session != {}:
        user = session['profile']['user_id']
        fm = FavoriteRecipeManager(user)
        recId = fm.getFavIdString()

    data = getRecipeDetail(recipe_id)
    similarRecipeID = getSimilarRecipeID(recipe_id)
    return render_template('recipe_detail.html', recipe=data, similarRecipeID=similarRecipeID, favs = recId)

@app.route("/profile")
@requires_auth
def profile():
    # pantry()
    # set user and create Pantry Manager
    user = "TestUser"  # for testing purposes
    if session != {}:
        user = session['profile']['user_id']
    pm = PantryManager(user)
    fm = FavoriteRecipeManager(user)

    pantryItems = pm.dispPantry()
    favItems = fm.dispFavorites()

    return render_template("profile.html", items = pantryItems, recipes = favItems)

@app.route("/pantry/add", methods=['POST'])
@requires_auth
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
        return redirect(url_for('profile'))
    else:
        return redirect(url_for('index'))

@app.route("/pantry/del", methods=['POST'])
@requires_auth
def pantryDel():
    # set user and create Pantry Manager
    user = "TestUser"  # for testing purposes
    if session != {}:
        user = session['profile']['user_id']
    pm = PantryManager(user)
    id = request.form['ingId']
    pm.delPantryItem(id)
    return redirect(url_for('profile'))


@app.route("/pantry/del_all/", methods=['POST'])
@requires_auth
def pantryDelAll():
    # set user and create Pantry Manager
    user = "TestUser"  # for testing purposes
    if session != {}:
        user = session['profile']['user_id']
    pm = PantryManager(user)
    pm.delPantryUser()
    return redirect(url_for('profile'))

@app.route('/favoriteThisRecipe', methods = ['POST'])
@requires_auth
def favoriteThisRecipe():
    userID = "TestUser"  # for testing purposes
    if session != {}:
        userID = session['profile']['user_id']
        # Take the given id and add it to the database
        db = FavoriteRecipeManager(userID)
        db.addFavoriteRecipe(request.form['favId'], request.form['favName'], request.form['favPic'])

    # temps for imported values
    data = ast.literal_eval(request.form["recipe"])
    similarRecipeID = request.form['similarRec']
    recId = db.getFavIdString()

    # now update the page to inform the user that they added the recipe to the database
    print("route ok")
    return render_template('recipe_detail.html', recipe=data, similarRecipeID=similarRecipeID,favs = recId, message="Add")

@app.route('/remove_recipe', methods = ['POST'])
@requires_auth
def removeFromFavorites():
    userID = "TestUser"  # for testing purposes
    if session != {}:
        userID = session['profile']['user_id']
    # Take the given id and remove from database
    db = FavoriteRecipeManager(userID)
    recipe_id = request.form['favId']
    db.delFavoriteRecipe(recipe_id)
    return redirect(url_for('profile'))

@app.route('/profile_favRemoveAll', methods = ['POST'])
@requires_auth
def removeAllFavs():
    userID = "TestUser"  # for testing purposes
    if session != {}:
        userID = session['profile']['user_id']
    # Take the given id and remove from database
    db = FavoriteRecipeManager(userID)
    db.delFavAll()
    return redirect(url_for('profile'))

@app.route("/detailDelFav", methods = ['POST'])
@requires_auth
def detailDelFav():

    userID = "TestUser"  # for testing purposes
    if session != {}:
        userID = session['profile']['user_id']
        # Take the given id and add it to the database
        db = FavoriteRecipeManager(userID)
        db.delFavoriteRecipe(request.form['favId'])

    # temps for imported values
    data = ast.literal_eval(request.form["recipe"])
    similarRecipeID = request.form['similarRec']
    recId = db.getFavIdString()

    return render_template('recipe_detail.html', recipe=data, similarRecipeID=similarRecipeID,favs = recId, message="Remove")



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
@requires_auth
def logout():
    session.clear()
    params = {'returnTo': url_for('index', _external=True),
              'client_id': AUTH0_CLIENT_ID}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


''' Retired Code - for ref if needed '''
# @app.route("/pantry")
# def pantry():
#     # set user and create Pantry Manager
#     user = "TestUser"  # for testing purposes
#     if session != {}:
#         user = session['profile']['user_id']
#     pm = PantryManager(user)

#     # pantry ingredients to show
#     pantryItems = pm.dispPantry()
#     return render_template("pantry.html", items=pantryItems)

# @app.route('/favorite_recipes')
# def getFavoriteRecipes():

#     userID = "TestUser"  # for testing purposes
#     if session != {}:
#         userID = session['profile']['user_id']
#     db = FavoriteRecipeManager(userID)
#     favRecipes = db.getFavoriteRecipes()
#     favRecipesList = favRecipes.split(", ")
#     favRecipesListFinal = []
#     # check for empty favorites list
#     for recipe in favRecipesList:
#         recipeSplit = recipe.split(" ")
#         title = recipeSplit[1:len(recipeSplit) - 1]
#         title = " ".join(map(str, title))
#         recipeDict = {"id": recipeSplit[0], "title": title,
#                   "image": recipeSplit[-1]}
#         favRecipesListFinal.append(recipeDict)


#     if favRecipesListFinal[0]['id'] != '':
#         return render_template('favorite_recipes.html', recipes=favRecipesListFinal)
#     else:
#         favRecipesListFinal = [] # otherwise this would be a dict with values
#         return render_template('favorite_recipes.html', recipes=favRecipesListFinal)