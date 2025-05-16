from . import db
from datetime import datetime

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    exercise = db.Column(db.String(100), nullable=False)

    # Strength fields
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    weights = db.Column(db.String(100))

    # Type of workout
    type = db.Column(db.String(20), nullable=False, default='strength')  # strength or cardio

    # Cardio fields
    distance = db.Column(db.String(20))  # e.g. '5 km'
    duration = db.Column(db.String(20))  # e.g. '00:25:00'
