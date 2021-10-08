from config import DB

# database class
class Pantry(DB.Model):
    id = DB.Column(DB.Integer, primary_key = True)
    userId = DB.Column(DB.Integer, nullable = False)
    ingId = DB.Column(DB.Integer, nullable = False)
    ingName = DB.Column(DB.String(100), nullable = False)
    ingPic = DB.Column(DB.String(200), nullable = False)