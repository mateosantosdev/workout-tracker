from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    workouts = db.relationship('Workout', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    exercise = db.Column(db.String(100), nullable=False)

    # Type of workout
    type = db.Column(db.String(20), nullable=False, default='strength')  # strength or cardio

    # Strength fields
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    weights = db.Column(db.String(100))

    # Cardio fields
    distance = db.Column(db.String(20))  # e.g. '5 km'
    duration = db.Column(db.String(20))  # e.g. '00:25:00'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
