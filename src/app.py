import requests
from flask import Flask, render_template, request, session, redirect, jsonify,\
    _request_ctx_stack, url_for
from spoon import searchRecipes
from os import environ as env
import json
from six.moves.urllib.request import urlopen
from six.moves.urllib.parse import urlencode
from functools import wraps
from flask_cors import cross_origin
from jose import jwt
from dotenv import load_dotenv, find_dotenv
from authlib.integrations.flask_client import OAuth
import constants

# Loading in Auth0 information from environment file
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
AUTH0_DOMAIN = env.get("AUTH0_DOMAIN")
AUTH0_AUDIENCE = env.get("AUTH0_IDENTIFIER")
SPOON_API_KEY = env.get("SPOON_KEY")
AUTH0_CALLBACK_URL = env.get("AUTH0_CALLBACK_URL")
AUTH0_CLIENT_ID = env.get("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = env.get("AUTH0_CLIENT_SECRET")
AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN
ALGO = ["RS256"]

# flask class instance
app = Flask(__name__)
oauth = OAuth(app)
auth0 = oauth.register(
    'auth0',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    api_base_url=AUTH0_BASE_URL,
    access_token_url=AUTH0_BASE_URL + '/oauth/token',
    authorize_url=AUTH0_BASE_URL + '/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)


# Error handler for user authorization
class AuthError(Exception):
    def __init__(self, error, code):
        self.error = error
        self.code = code

@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.code
    return response

# Format error response and append status code
def get_token_auth_header():
    """
    Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                        "description":
                            "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must start with"
                            " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                        "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must be"
                            " Bearer token"}, 401)

    token = parts[1]
    return token


def requires_scope(required_scope):
    """
    Determines if the required scope is present in the Access Token
    Args:
        required_scope (str): The scope required to access the resource
    """
    token = get_token_auth_header()
    unverified_claims = jwt.get_unverified_claims(token)
    if unverified_claims.get("scope"):
            token_scopes = unverified_claims["scope"].split()
            for token_scope in token_scopes:
                if token_scope == required_scope:
                    return True
    return False


def requires_auth(f):
    """
    Determines if the Access Token is valid
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGO,
                    audience=AUTH0_AUDIENCE,
                    issuer="https://"+AUTH0_DOMAIN+"/"
                )
            except jwt.ExpiredSignatureError:
                raise AuthError({"code": "token_expired",
                                "description": "token is expired"}, 401)
            except jwt.JWTClaimsError:
                raise AuthError({"code": "invalid_claims",
                                "description":
                                    "incorrect claims,"
                                    "please check the audience and issuer"}, 401)
            except Exception:
                raise AuthError({"code": "invalid_header",
                                "description":
                                    "Unable to parse authentication"
                                    " token."}, 401)

            _request_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)
        raise AuthError({"code": "invalid_header",
                        "description": "Unable to find appropriate key"}, 401)
    return decorated

# Controllers API
@app.route("/api/public")
@cross_origin(headers=["Content-Type", "Authorization"])
def public():
    """
    No access token required to access this route
    """
    response = "Hello from a public endpoint! You don't need to be authenticated to see this."
    return jsonify(message=response)


@app.route("/api/private")
@cross_origin(headers=["Content-Type", "Authorization"])
@cross_origin(headers=["Access-Control-Allow-Origin", "http://localhost:5000"])
@requires_auth
def private():
    """
    A valid access token is required to access this route
    """
    response = "Hello from a private endpoint! You need to be authenticated to see this."
    return jsonify(message=response)


@app.route("/api/private-scoped")
@cross_origin(headers=["Content-Type", "Authorization"])
@cross_origin(headers=["Access-Control-Allow-Origin", "http://localhost:5000"])
@requires_auth
def private_scoped():
    """
    A valid access token and an appropriate scope are required to access this route
    """
    if requires_scope("read:messages"):
        response = "Hello from a private endpoint! You need to be authenticated and have a scope of read:messages to see this."
        return jsonify(message=response)
    raise AuthError({
        "code": "Unauthorized",
        "description": "You don't have access to this resource"
    }, 403)

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


@app.route("/recipe/<recipe_id>")
def getRecipeDetail(recipe_id):
    req = f'https://api.spoonacular.com/recipes/{recipe_id}/information?&apiKey={SPOON_API_KEY}'
    res = requests.get(req)
    data = res.json()
    return render_template('recipe_detail.html', recipe=data)

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
    params = {'returnTo': url_for('index', _external=True), 'client_id': AUTH0_CLIENT_ID}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

# test module import
if __name__ == "__main__":
    app.secret_key="super secret key"
    app.run(debug = True)