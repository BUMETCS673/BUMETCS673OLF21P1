import requests
from dotenv import find_dotenv, load_dotenv
from os import environ as env
from config import API_KEY

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
SPOON_API_KEY = env.get("SPOON_KEY")

def searchRecipes(ingredients, diet, intolerances):
    # basic request
    req = f'https://api.spoonacular.com/recipes/complexSearch?' \
          f'includeIngredients={ingredients}&apiKey={SPOON_API_KEY}'

    if diet == 'all':
        # do nothing
        pass
    else:
        # either vegan, vegetarian, glutenfree, ketogenic, whole30,
        # lacto-vegetarian, pescetarian, ovo-vegetarian, primal, paleo
        req += f'&diet={diet}' 

    if intolerances == 'no-intol':
        pass
    else:
        # dairy, egg, gluten, grain, peanut, seafood, sesame, shellfish
        intolerances += f'&intolerances={intolerances}'

    res = requests.get(req)
    # json decode method, turn data into a native python datatype
    data = res.json()
    print(data)
    results = data['results']
    print(results)
    return results

def getRecipeDetail(recipe_id):
    req = f'https://api.spoonacular.com/recipes/{recipe_id}/information?&apiKey={API_KEY}'
    res = requests.get(req)
    data = res.json()
    return data

def searchSpoon(ingredient):
    # api url
    ingUrl = 'https://api.spoonacular.com/food/ingredients/search?query={}&apiKey={}&number=1'

    search = requests.get(ingUrl.format(ingredient, API_KEY)).json()

    # search spoonable API to verify actual ingredient
    if search['totalResults'] > 0:
        ingName = ingredient.lower()
        ingId = search['results'][0]['id']
        ingPic = search['results'][0]['image']
        return [ingName, ingId, ingPic]
    else:

        return False