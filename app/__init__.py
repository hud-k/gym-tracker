from flask import Flask, render_template, request
def create_app():
    app = Flask(__name__)

    @app.route("/")
    def homepage():
        return render_template("home.html")

    @app.route("/register")
    def register():
        return render_template("register.html")
    
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