from flask import Flask, render_template
import sqlalchemy

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def homepage():
        return render_template("home.html")
    
    @app.route("/about")
    def about():
        return "practicing routes"
    
    @app.route("/secret")
    def secret():
        return "you shouldnt be here!"

    return app