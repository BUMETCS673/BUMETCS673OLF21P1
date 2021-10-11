from config import app, DB, AUTH0_CLIENT_SECRET
import routes

if __name__ == '__main__':
    # create database - will add new models if needed
    DB.create_all()

    # start the app
    app.run(debug=True, host = '127.0.0.1')
