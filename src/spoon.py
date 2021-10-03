import requests
import os

API_KEY = os.environ.get('SPOONACULAR_API_KEY')
BASE_URL = os.environ.get('SPOONACULAR_API_BASE_URL')

def searchRecipes(ingredients, diet, intolerances):
    # basic request
    req = f'{BASE_URL}/recipes/complexSearch?includeIngredients={ingredients}&apiKey={API_KEY}'

    if diet == 'all':
        pass  # do nothing
    else:  # either vegan, vegetarian, glutenfree, ketogenic, whole30, lacto-vegetarian, pescetarian, ovo-vegetarian, primal, paleo
        req += f'&diet={diet}'

    if intolerances == 'no-intol':
        pass
    else: # dairy, egg, gluten, grain, peanut, seafood, sesame, shellfish
        intolerances += f'&intolerances={intolerances}'

    res = requests.get(req)
    data = res.json() # json decode method, turn data into a native python datatype
    print(data)
    results = data['results']
    print(results)
    return results


def get_recipe_by_id(recipe_id):
    request_url = f'{BASE_URL}/recipes/{recipe_id}/information?&apiKey={API_KEY}'
    res = requests.get(url=request_url)
    return res.json()
