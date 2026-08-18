from app import db
from flask_login import UserMixin

class Users(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(20), unique=True)
        password = db.Column(db.String(100))

        def __init__(self, username, password):
            self.username = username
            self.password = password

class Workout(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
      exercise_name = db.Column(db.String(100))
      weight = db.Column(db.Float)
      sets = db.Column(db.Integer)
      reps = db.Column(db.Integer)
      date = db.Column(db.Date)

      def __init__(self, user_id, exercise_name, weight, sets, reps, date):
            self.user_id = user_id
            self.exercise_name = exercise_name
            self.weight = weight
            self.sets = sets
            self.reps = reps
            self.date = date