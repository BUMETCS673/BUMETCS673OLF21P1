import requests


def searchRecipes(ingredients, diet, intolerance):
    # API information
    API_KEY = '9e749e7df97047c38000f0f4addb64f9'
    
    # basic request
    req = f'https://api.spoonacular.com/recipes/&apiKey={API_KEY}complexSearch?includeIngredients={ingredients}'

    if diet == 'all':
        pass  # do nothing
    else:  # either vegan, vegetarian, glutenfree, ketogenic, whole30, lacto-vegetarian, pescetarian, ovo-vegetarian, primal, paleo
        req += f'&diet={diet}' 

    if intolerance == 'no-intol':
        pass
    else: # dairy, egg, gluten, grain, peanut, seafood, sesame, shellfish
        intolerance += f'&intolerance={intolerance}'

    res = requests.get(req)
    data = res.json() # json decode method, turn data into a native python datatype 
    print(data)
    hits = data['hits']
    print(data)
    return hits