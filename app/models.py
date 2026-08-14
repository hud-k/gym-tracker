from app import db
from flask_login import UserMixin

class Users(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(20), unique=True)
        password = db.Column(db.String(100))

        def __init__(self, username, password):
            self.username = username
            self.password = password