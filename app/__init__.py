from flask import Flask, render_template
import sqlalchemy

def create_app():
    app = Flask(__name__)

    @app.route("/home")
    def homepage():
        return render_template("home.html")
    
    @app.route("/login")
    def login():
        return render_template("login.html")
    
    @app.route("/log-workout")
    def log_workout():
        return render_template("log_workout.html")

    @app.route("/history")
    def history():
        return render_template("history.html")

    return app