from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# flask class instance
app = Flask(__name__)

# api key:
API_KEY = '9e749e7df97047c38000f0f4addb64f9'


# database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cheffy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(app)
