import requests

from config import SPOON_API_KEY


def searchRecipes(ingredients, diet, intolerances):
    # basic request
    req = f'https://api.spoonacular.com/recipes/complexSearch?' \
          f'includeIngredients={ingredients}&apiKey={SPOON_API_KEY}'

    # do nothing
    if diet is None:
        pass
    # either vegan, vegetarian, glutenfree, ketogenic, whole30,
    # lacto-vegetarian, pescetarian, ovo-vegetarian, primal, paleo
    else:
        req += f'&diet={diet}'

    if intolerances is None:
        pass
    # dairy, egg, gluten, grain, peanut, seafood, sesame, shellfish
    else:
        intolerances += f'&intolerances={intolerances}'

    res = requests.get(req)
    # json decode method, turn data into a native python datatype
    data = res.json()
    print(data)
    results = data['results']
    print(results)
    return results


def getRecipeDetail(recipe_id):
    req = f'https://api.spoonacular.com/recipes/{recipe_id}/' \
          f'information?&apiKey={SPOON_API_KEY}'
    res = requests.get(req)
    data = res.json()
    return data


def searchSpoon(ingredient):
    # api url
    ingUrl = 'https://api.spoonacular.com/food/ingredients/search?query={}&' \
             'apiKey={}&number=1'

    search = requests.get(ingUrl.format(ingredient, SPOON_API_KEY)).json()

    # search spoonable API to verify actual ingredient
    if search['totalResults'] > 0:
        ingName = ingredient.lower()
        ingId = search['results'][0]['id']
        ingPic = search['results'][0]['image']
        return [ingName, ingId, ingPic]
    else:

        return False
