from flask import Blueprint, render_template, request, redirect, url_for, session, abort
from .models import db, Workout, User
from datetime import datetime, timedelta

main = Blueprint('main', __name__)

def format_date_pretty(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    return date.strftime("%d %B %Y")  # e.g. 16 May 2025

@main.route('/')
def index():
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    else:
        return redirect(url_for('auth.login'))
    
    date_str = request.args.get("date", datetime.today().strftime("%Y-%m-%d"))
    formatted_date = format_date_pretty(date_str)
    workouts = workouts = Workout.query.filter_by(date=date_str, user_id=user.id).all()

    prev_date = (datetime.strptime(date_str, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
    next_date = (datetime.strptime(date_str, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")

    return render_template("index.html", date=date_str, formatted_date=formatted_date, workouts=workouts, prev_date=prev_date, next_date=next_date)


@main.route('/add', methods=['GET', 'POST'])
def add_workout():
    if request.method == 'POST':
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        exercise = request.form['exercise']
        workout_type = request.form['type']
        user_id = session['user_id']

        if workout_type == 'cardio':
            distance = request.form.get('distance', '')
            duration = request.form.get('duration', '')
            new_workout = Workout(
                date=date,
                exercise=exercise,
                type='cardio',
                distance=distance,
                duration=duration,
                sets=0,
                reps=0,
                weights=None,
                user_id=user_id
            )
        else:
            sets = int(request.form['sets'])
            reps = int(request.form['reps'])
            weight_inputs = [
                request.form.get(f'weight{i+1}', '').strip()
                for i in range(sets)
            ]
            weights = '/'.join([w for w in weight_inputs if w])
            new_workout = Workout(
                date=date,
                exercise=exercise,
                type='strength',
                sets=sets,
                reps=reps,
                weights=weights if weights else None,
                distance=None,
                duration=None,
                user_id=user_id
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
    if workout.user_id != session['user_id']:
        abort(403)

    if request.method == 'POST':
        workout.exercise = request.form['exercise']
        workout.type = request.form['type']

        if workout.type == 'strength':
            workout.sets = int(request.form['sets']) if request.form['sets'] else 0
            workout.reps = int(request.form['reps']) if request.form['reps'] else 0

            weight_inputs = [
                request.form.get(f'weight{i+1}', '').strip()
                for i in range(workout.sets)
            ]
            workout.weights = '/'.join([w for w in weight_inputs if w]) or None

            # Clear cardio fields
            workout.distance = None
            workout.duration = None

        elif workout.type == 'cardio':
            workout.sets = 0
            workout.reps = 0
            workout.weights = None
            workout.distance = request.form.get('distance', '')
            workout.duration = request.form.get('duration', '')

        db.session.commit()
        return redirect(url_for('main.index', date=workout.date.isoformat()))

    date_str = workout.date.strftime('%Y-%m-%d')
    formatted_date = format_date_pretty(date_str)
    return render_template("new_workout.html", date=date_str, formatted_date=formatted_date, workout=workout)


@main.route('/delete/<int:workout_id>', methods=['POST'])
def delete_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    if workout.user_id != session['user_id']:
        abort(403)

    date = workout.date.isoformat()
    db.session.delete(workout)
    db.session.commit()
    return redirect(url_for('main.index', date=date))
