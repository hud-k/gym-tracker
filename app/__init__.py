from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import werkzeug.security

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Acer/Desktop/gym-tracker/instance/gymtracker.db'
    db.init_app(app)

    class Users(db.Model):
        _id = db.Column("id", db.Integer, primary_key=True)
        username = db.Column(db.String(20))
        password = db.Column(db.String(100))

        def __init__(self, username, password):
            self.username = username
            self.password = password
            
    with app.app_context():
            db.create_all()
            
    @app.route("/")
    def homepage():
        return render_template("home.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            hashed_password = werkzeug.security.generate_password_hash(password)

            new_user = Users(username, hashed_password)
            db.session.add(new_user)
            db.session.commit()


            return render_template("register.html", message="Successfully created account!")
        return render_template("register.html", message="")
    
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            return "You submitted information"
            
        return render_template("login.html")
    
    @app.route("/log-workout")
    def log_workout():
        return render_template("log_workout.html")

    @app.route("/history")
    def history():
        return render_template("history.html")

    return app