"""
Finds and returns a specific recipe
"""

import requests


def searchForRecipe(recipe_search):
    """When given a recipe name this function will return a recipe from spoonacular"""

    # API information
    API_KEY = '9e749e7df97047c38000f0f4addb64f9'

    # Basic request
    number = 3
    req = f'https://api.spoonacular.com/recipes/complexSearch?query={recipe_search}&number={number}&apiKey={API_KEY}'

    res = requests.get(req)
    data = res.json()  # json decode method, turn data into a native python datatype
    print(data)  # DEBUG
    results = data['results']
    print(results)  # DEBUG
    return results


def getRecipeInformation(recipe_id):
    """When given a recipe ID, returns the detailed recipe info"""

    # API information
    API_KEY = '9e749e7df97047c38000f0f4addb64f9'

    # Get recipe information
    req = f'https://api.spoonacular.com/recipes/{recipe_id}/information?&apiKey={API_KEY}'

    res = requests.get(req)
    data = res.json()  # json decode method, turn data into a native python datatype
    print(data)  # DEBUG
    return data
