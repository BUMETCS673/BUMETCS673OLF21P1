import json
from functools import wraps
from urllib.request import urlopen

from authlib.jose import jwt
from flask import jsonify, _request_ctx_stack, request, session, redirect
from flask_cors import cross_origin
from werkzeug.exceptions import HTTPException

from config import app, AUTH0_CLIENT_SECRET, AUTH0_CLIENT_ID, AUTH0_AUDIENCE,\
    AUTH0_DOMAIN, AUTH0_CALLBACK_URL, AUTH0_BASE_URL, ALGO
from authlib.integrations.flask_client import OAuth

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

@app.errorhandler(Exception)
def handle_auth_error(ex):
    response = jsonify(message=str(ex))
    response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
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
  @wraps(f)
  def decorated(*args, **kwargs):
    if 'profile' not in session:
      # Redirect to Login page here
      return redirect('/login')
    return f(*args, **kwargs)

  return decorated

# def requires_auth(f):
#     """
#     Determines if the Access Token is valid
#     """
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         auth = request.headers.get("Authorization", None)
#         if auth is None:
#             return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL,
#                                      audience=AUTH0_AUDIENCE)
#         token = get_token_auth_header()
#         jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
#         jwks = json.loads(jsonurl.read())
#         unverified_header = jwt.get_unverified_header(token)
#         rsa_key = {}
#         for key in jwks["keys"]:
#             if key["kid"] == unverified_header["kid"]:
#                 rsa_key = {
#                     "kty": key["kty"],
#                     "kid": key["kid"],
#                     "use": key["use"],
#                     "n": key["n"],
#                     "e": key["e"]
#                 }
#         if rsa_key:
#             try:
#                 payload = jwt.decode(
#                     token,
#                     rsa_key,
#                     algorithms=ALGO,
#                     audience=AUTH0_AUDIENCE,
#                     issuer="https://"+AUTH0_DOMAIN+"/"
#                 )
#             except jwt.ExpiredSignatureError:
#                 raise AuthError({"code": "token_expired",
#                                 "description": "token is expired"}, 401)
#             except jwt.JWTClaimsError:
#                 raise AuthError({"code": "invalid_claims",
#                                 "description":
#                                     "incorrect claims,"
#                                     "please check the audience and issuer"},
#                                 401)
#             except Exception:
#                 raise AuthError({"code": "invalid_header",
#                                 "description":
#                                     "Unable to parse authentication"
#                                     " token."}, 401)

#             _request_ctx_stack.top.current_user = payload
#             return f(*args, **kwargs)
#         raise AuthError({"code": "invalid_header",
#                         "description": "Unable to find appropriate key"}, 401)
#     return decorated

# Controllers API
@app.route("/api/public")
@cross_origin(headers=["Content-Type", "Authorization"])
def public():
    """
    No access token required to access this route
    """
    response = "Hello from a public endpoint! You don't need to be" \
               " authenticated to see this."
    return jsonify(message=response)


@app.route("/api/private")
@cross_origin(headers=["Content-Type", "Authorization"])
@cross_origin(headers=["Access-Control-Allow-Origin", "http://localhost:5000"])
@requires_auth
def private():
    """
    A valid access token is required to access this route
    """
    response = "Hello from a private endpoint! You need to be authenticated" \
               " to see this."
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
        response = "Hello from a private endpoint! You need to be" \
                   " authenticated and have a scope of read:messages to see" \
                   " this."
        return jsonify(message=response)
    raise AuthError({
        "code": "Unauthorized",
        "description": "You don't have access to this resource"
    }, 403)