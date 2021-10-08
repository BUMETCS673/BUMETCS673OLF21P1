from config import app, DB

if __name__ == '__main__':
    # create database - will add new models if needed
    DB.create_all()

    # start the app
    app.run(debug=True)
