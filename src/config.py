from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import environ as env
from dotenv import load_dotenv, find_dotenv

# Importing environment variables (API keys and other secure info)
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



# database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cheffy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(app)
