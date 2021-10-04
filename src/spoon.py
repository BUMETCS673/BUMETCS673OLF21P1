import requests
from dotenv import find_dotenv, load_dotenv
from os import environ as env

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
SPOON_API_KEY = env.get("SPOON_KEY")

def searchRecipes(ingredients, diet, intolerances):

    # basic request
    req = f'https://api.spoonacular.com/recipes/complexSearch?include' \
          f'Ingredients={ingredients}&apiKey={SPOON_API_KEY}'

    if diet == 'all':
        pass  # do nothing
    # either vegan, vegetarian, glutenfree, ketogenic, whole30,
    # lacto-vegetarian, pescetarian, ovo-vegetarian, primal, paleo
    else:
        req += f'&diet={diet}'

    if intolerances == 'no-intol':
        pass
    else:  # dairy, egg, gluten, grain, peanut, seafood, sesame, shellfish
        intolerances += f'&intolerances={intolerances}'

    res = requests.get(req)
    # json decode method, turn data into a native python datatype
    data = res.json()
    print(data)
    results = data['results']
    print(results)
    return results


def getRecipeById(recipeID):
    """Return the recipe detail using a recipe ID."""

    request_url = f'https://api.spoonacular.com/recipes/{recipeID}/' \
                  f'information?&apiKey={SPOON_API_KEY}'
    res = requests.get(url=request_url)
    return res.json()
