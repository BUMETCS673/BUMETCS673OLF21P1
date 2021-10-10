from config import app, DB, AUTH0_CLIENT_SECRET
import routes

if __name__ == '__main__':
    # create database - will add new models if needed
    DB.create_all()

    # give the app the auth0 key
    # app.secret_key = AUTH0_CLIENT_SECRET

    # start the app
    app.run(debug=True, host = '127.0.0.1')
