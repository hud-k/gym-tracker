from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import werkzeug.security
from datetime import datetime

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Acer/Desktop/gym-tracker/instance/gymtracker.db'
    app.config['SECRET_KEY'] = 'testsecretdevkey'
    db.init_app(app)
    from app.models import Users, Workout
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))
            
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
            existing_user = Users.query.filter_by(username=username).first()
            if existing_user:
                return render_template("register.html", message="That username is already taken.")
            else:
                hashed_password = werkzeug.security.generate_password_hash(password)
                new_user = Users(username, hashed_password)
                db.session.add(new_user)
                db.session.commit()

                return render_template("register.html", message="Successfully created account!")
        return render_template("register.html", message="")
    
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            user = Users.query.filter_by(username=username).first()

            if user and werkzeug.security.check_password_hash(user.password, password):
                login_user(user)
                return render_template("login.html", message="Successfully logged in.")
            else:
                return render_template("login.html", message="Incorrect username or password.")
            
        return render_template("login.html", message="")
    
    @app.route("/log-workout", methods=["GET", "POST"])
    @login_required
    def log_workout():
        if request.method == "POST":
            user_id = current_user.id
            exercise = request.form["exercise_name"]
            weight = float(request.form["weight"])
            sets = int(request.form["sets"])
            reps = int(request.form["reps"])
            date = datetime.strptime(request.form["date"], "%Y-%m-%d").date()

            new_exercise = Workout(user_id, exercise, weight, sets, reps, date)
            db.session.add(new_exercise)
            db.session.commit()

            return render_template("log_workout.html", message=f"{exercise} was logged.")
        return render_template("log_workout.html")

    @app.route("/history")
    @login_required
    def history():
        workouts = Workout.query.filter_by(user_id=current_user.id).all()
        return render_template("history.html", workouts=workouts)

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("login"))

    @app.route("/delete/<int:workout_id>")
    @login_required
    def delete_workout(workout_id):
        workout_to_delete = Workout.query.filter_by(id=workout_id, user_id=current_user.id).first()
        if workout_to_delete:
            db.session.delete(workout_to_delete)
            db.session.commit()
        return redirect(url_for("history"))

    @app.route("/edit/<int:workout_id>", methods=["GET", "POST"])
    @login_required
    def edit_workout(workout_id):
        workout_to_edit = Workout.query.filter_by(id=workout_id, user_id=current_user.id).first()
        if workout_to_edit is None:
            return redirect(url_for("history"))
        
        if request.method == "POST":
            form = request.form
            workout_to_edit.exercise_name = form["exercise_name"]
            workout_to_edit.weight = float(form["weight"])
            workout_to_edit.sets = int(form["sets"])
            workout_to_edit.reps = int(form["reps"])
            workout_to_edit.date = datetime.strptime(form["date"], "%Y-%m-%d").date()
            db.session.commit()
            return redirect(url_for("history"))

        return render_template("edit_workout.html", workout=workout_to_edit)

    return app