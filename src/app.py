from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import SessionLocal
from models import User, Exercise, WorkoutSession, WorkoutDetail
from utils import hash_password, verify_password
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this!

# Flask-SQLAlchemy session setup
db_session = SessionLocal()

# Routes

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed = hash_password(password)
        new_user = User(username=username, email=email, password_hash=hashed)
        db_session.add(new_user)
        try:
            db_session.commit()
            flash('User registered successfully! Please login.', 'success')
            return redirect(url_for('login'))
        except IntegrityError:
            db_session.rollback()
            flash('Username or email already exists!', 'danger')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db_session.query(User).filter(User.username == username).first()
        if user and verify_password(password, user.password_hash):
            session['user_id'] = user.user_id
            session['username'] = user.username
            flash(f'Welcome, {user.username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/log_workout', methods=['GET', 'POST'])
def log_workout():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    exercises = db_session.query(Exercise).all()
    if request.method == 'POST':
        session_date = request.form['session_date']
        notes = request.form['notes']
        workout_session = WorkoutSession(
            user_id=session['user_id'], 
            session_date=session_date, 
            notes=notes
        )
        db_session.add(workout_session)
        db_session.commit()
        
        for exercise_id in request.form.getlist('exercise_id'):
            sets = request.form.get(f'sets_{exercise_id}')
            repetitions = request.form.get(f'repetitions_{exercise_id}')
            weight = request.form.get(f'weight_{exercise_id}')
            duration = request.form.get(f'duration_{exercise_id}')
            distance = request.form.get(f'distance_{exercise_id}')
            
            workout_detail = WorkoutDetail(
                session_id=workout_session.session_id,
                exercise_id=exercise_id,
                sets=sets,
                repetitions=repetitions,
                weight=weight,
                duration=duration,
                distance=distance
            )
            db_session.add(workout_detail)
        db_session.commit()
        flash('Workout logged successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('log_workout.html', exercises=exercises)

@app.route('/view_progress')
def view_progress():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    sessions = db_session.query(WorkoutSession).filter(WorkoutSession.user_id == user_id).all()
    return render_template('view_progress.html', sessions=sessions)

if __name__ == '__main__':
    app.run(debug=True)
