from datetime import datetime, timedelta
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation

def format_date_pretty(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    return date.strftime("%d %B %Y")  # e.g. 16 May 2025


def format_duration(minutes):
    hours, mins = divmod(round(minutes), 60)
    if hours == 0:
        return f"{mins} min"
    if mins == 0:
        return f"{hours} hr"
    return f"{hours} hr {mins} min"

def get_exercise_count_by_day(workouts, start_date, days=7):
    day_labels = [(start_date + timedelta(days=i)).strftime('%d/%m') for i in range(days)]
    date_counts = Counter([w.date for w in workouts])
    workouts_count_list = [date_counts.get(start_date + timedelta(days=i), 0) for i in range(days)]
    return day_labels, workouts_count_list


def get_daily_durations(exercises, start_date, day_span):
    daily_totals = defaultdict(int)

    for exercise in exercises:
        exercise_date = exercise.date  # Ensure we strip time
        if start_date <= exercise_date <= start_date + timedelta(days=day_span):
            daily_totals[exercise_date] += exercise.duration or 0  # Fallback to 0 if null

    return daily_totals


def get_total_cardio_distance(exercises):
    total_distance = 0
    for ex in exercises:
        if ex.type == 'cardio' and ex.distance:
            total_distance += float(ex.distance)
    return total_distance

def get_total_strength_volume(exercises):
    total_volume = 0
    for ex in exercises:
        if ex.type == 'strength' and ex.reps and ex.weights:
            try:
                weights = [int(w) for w in ex.weights.split('/') if w.strip().isdigit()]
                for weight in weights:
                    total_volume += weight * ex.reps
            except ValueError:
                continue
    return total_volume

def get_time_per_type(exercises):
    totals = defaultdict(int)

    # Sum durations by type
    for ex in exercises:
        totals[ex.type] += ex.duration or 0

    # Total time (in minutes)
    total_time = sum(totals.values()) or 1  # avoid division by zero

    # Calculate percentages and formatted durations
    workout_type_percentages = {
        type_: round((duration / total_time) * 100, 1)
        for type_, duration in totals.items()
    }

    workout_type_durations = {
        type_: format_duration(duration)
        for type_, duration in totals.items()
    }

    return workout_type_percentages, workout_type_durations

def format_pace(pace):
    if pace is None:
        return "N/A"
    minutes = int(pace)
    seconds = round((pace - minutes) * 60)
    return f"{minutes}m {seconds}s /km"

def get_fastest_pace(exercises):
    fastest = None
    for ex in exercises:
        if ex.type == 'cardio' and ex.distance and ex.duration:
            try:
                km = float(ex.distance)
                if km > 0:
                    pace = ex.duration / km  # minutes per km
                    if fastest is None or pace < fastest:
                        fastest = pace
            except (ValueError, IndexError):
                continue
    return format_pace(fastest)  # e.g. 5.4 means 5 mins 24 secs