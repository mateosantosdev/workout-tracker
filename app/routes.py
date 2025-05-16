from flask import Blueprint, render_template, request, redirect, url_for
from .models import db, Workout
from datetime import datetime, timedelta
from datetime import datetime

main = Blueprint('main', __name__)

def format_date_pretty(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    return date.strftime("%d %B %Y")  # e.g. 16 May 2025

@main.route('/')
def index():
    date_str = request.args.get("date", datetime.today().strftime("%Y-%m-%d"))
    formatted_date = format_date_pretty(date_str)
    workouts = Workout.query.filter_by(date=date_str).all()

    prev_date = (datetime.strptime(date_str, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
    next_date = (datetime.strptime(date_str, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")

    return render_template("index.html", date=date_str, formatted_date=formatted_date, workouts=workouts, prev_date=prev_date, next_date=next_date)


@main.route('/add', methods=['GET', 'POST'])
def add_workout():
    if request.method == 'POST':
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        exercise = request.form['exercise']
        sets = int(request.form['sets'])
        reps = int(request.form['reps'])

        # Collect weights (optional)
        weight_inputs = [
            request.form.get('weight1', '').strip(),
            request.form.get('weight2', '').strip(),
            request.form.get('weight3', '').strip(),
            request.form.get('weight4', '').strip(),
        ]
        weights = '/'.join([w for w in weight_inputs if w])

        new_workout = Workout(
            date=date,
            exercise=exercise,
            sets=sets,
            reps=reps,
            weights=weights if weights else None
        )
        db.session.add(new_workout)
        db.session.commit()

        return redirect(url_for('main.index', date=date.isoformat()))

    date_str = request.args.get("date", datetime.today().strftime("%Y-%m-%d"))
    formatted_date = format_date_pretty(date_str)
    return render_template("new_workout.html", date=date_str, formatted_date=formatted_date)

@main.route('/edit/<int:workout_id>', methods=['GET', 'POST'])
def edit_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)

    if request.method == 'POST':
        workout.exercise = request.form['exercise']
        workout.sets = int(request.form['sets'])
        workout.reps = int(request.form['reps'])

        # Collect weights
        weight_inputs = [
            request.form.get(f'weight{i+1}', '').strip()
            for i in range(workout.sets)
        ]
        workout.weights = '/'.join([w for w in weight_inputs if w]) or None

        db.session.commit()
        return redirect(url_for('main.index', date=workout.date.isoformat()))

    date_str = workout.date.strftime('%Y-%m-%d')
    formatted_date = format_date_pretty(date_str)
    return render_template("new_workout.html", date=date_str, formatted_date=formatted_date, workout=workout)


@main.route('/delete/<int:workout_id>', methods=['POST'])
def delete_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    date = workout.date.isoformat()
    db.session.delete(workout)
    db.session.commit()
    return redirect(url_for('main.index', date=date))
