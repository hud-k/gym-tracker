from flask import Flask
import sqlalchemy

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def homepage():
        return "Hello World!"
    
    @app.route("/about")
    def about():
        return "practicing routes"
    
    @app.route("/secret")
    def secret():
        return "you shouldnt be here!"

    return app