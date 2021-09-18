from flask import Flask, render_template, request

# flask class instance
app = Flask(__name__)

# / route will show our index template
@app.route("/")
def index():
    return render_template("index.html")

# /about will show about page
app.route("/about")
def about():
    return render_template("about.html")

# test module import
if __name__ == "__main__":
    app.run(debug = True)