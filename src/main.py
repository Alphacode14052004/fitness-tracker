# main.py
from database import SessionLocal, engine
from models import Base, User, Exercise, WorkoutSession, WorkoutDetail
from utils import hash_password, verify_password
from sqlalchemy.exc import IntegrityError
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate
from datetime import datetime

# Create all tables
Base.metadata.create_all(bind=engine)

def create_user(session):
    username = input("Enter username: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    hashed = hash_password(password)
    user = User(username=username, email=email, password_hash=hashed)
    session.add(user)
    try:
        session.commit()
        print("User created successfully.")
    except IntegrityError:
        session.rollback()
        print("Username or email already exists.")

def login(session):
    username = input("Enter username: ")
    password = input("Enter password: ")
    user = session.query(User).filter(User.username == username).first()
    if user and verify_password(password, user.password_hash):
        print(f"Welcome, {user.username}!")
        return user
    else:
        print("Invalid credentials.")
        return None

def add_exercise(session):
    name = input("Exercise name: ")
    category = input("Category (Strength/Cardio/Flexibility): ")
    description = input("Description: ")
    exercise = Exercise(name=name, category=category, description=description)
    session.add(exercise)
    session.commit()
    print("Exercise added.")

def list_exercises(session):
    exercises = session.query(Exercise).all()
    data = [(ex.exercise_id, ex.name, ex.category) for ex in exercises]
    print(tabulate(data, headers=["ID", "Name", "Category"]))

def log_workout(session, user):
    session_date = input("Enter date (YYYY-MM-DD) or leave blank for today: ")
    if not session_date:
        session_date = datetime.today().strftime('%Y-%m-%d')
    notes = input("Any notes for this session? ")
    workout_session = WorkoutSession(user_id=user.user_id, session_date=session_date, notes=notes)
    session.add(workout_session)
    session.commit()
    print("Workout session created.")
    
    while True:
        add_detail = input("Add exercise to this session? (y/n): ").lower()
        if add_detail != 'y':
            break
        list_exercises(session)
        exercise_id = int(input("Enter Exercise ID: "))
        sets = input("Sets (leave blank if not applicable): ")
        repetitions = input("Repetitions (leave blank if not applicable): ")
        weight = input("Weight used (kg/lbs, leave blank if not applicable): ")
        duration = input("Duration in seconds (leave blank if not applicable): ")
        distance = input("Distance (km/miles, leave blank if not applicable): ")
        
        detail = WorkoutDetail(
            session_id=workout_session.session_id,
            exercise_id=exercise_id,
            sets=int(sets) if sets else None,
            repetitions=int(repetitions) if repetitions else None,
            weight=float(weight) if weight else None,
            duration=int(duration) if duration else None,
            distance=float(distance) if distance else None
        )
        session.add(detail)
        session.commit()
        print("Exercise added to session.")

def view_progress(session, user):
    data = session.query(WorkoutSession).filter(WorkoutSession.user_id == user.user_id).all()
    if not data:
        print("No workout sessions found.")
        return
    records = []
    for ws in data:
        for wd in ws.workout_details:
            records.append({
                "Date": ws.session_date,
                "Exercise": wd.exercise.name,
                "Sets": wd.sets,
                "Reps": wd.repetitions,
                "Weight": wd.weight,
                "Duration": wd.duration,
                "Distance": wd.distance
            })
    df = pd.DataFrame(records)
    print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
    
    # Example Visualization: Progress Over Time for a Specific Exercise
    exercise_name = input("Enter exercise name to visualize progress (or leave blank to skip): ")
    if exercise_name:
        exercise = session.query(Exercise).filter(Exercise.name == exercise_name).first()
        if not exercise:
            print("Exercise not found.")
            return
        details = session.query(WorkoutDetail).join(WorkoutSession).filter(
            WorkoutDetail.exercise_id == exercise.exercise_id,
            WorkoutSession.user_id == user.user_id,
            WorkoutDetail.weight != None
        ).order_by(WorkoutSession.session_date).all()
        if not details:
            print("No weight data for this exercise.")
            return
        dates = [d.session.session_date for d in details]
        weights = [float(d.weight) for d in details]
        plt.plot(dates, weights, marker='o')
        plt.title(f'Progress for {exercise.name}')
        plt.xlabel('Date')
        plt.ylabel('Weight Used')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

def main():
    session = SessionLocal()
    user = None
    while True:
        if not user:
            print("\n--- Fitness Tracker ---")
            print("1. Create User")
            print("2. Login")
            print("3. Exit")
            choice = input("Choose an option: ")
            if choice == '1':
                create_user(session)
            elif choice == '2':
                user = login(session)
            elif choice == '3':
                break
            else:
                print("Invalid choice.")
        else:
            print(f"\n--- Welcome, {user.username} ---")
            print("1. Add Exercise")
            print("2. List Exercises")
            print("3. Log Workout")
            print("4. View Progress")
            print("5. Logout")
            choice = input("Choose an option: ")
            if choice == '1':
                add_exercise(session)
            elif choice == '2':
                list_exercises(session)
            elif choice == '3':
                log_workout(session, user)
            elif choice == '4':
                view_progress(session, user)
            elif choice == '5':
                user = None
                print("Logged out.")
            else:
                print("Invalid choice.")

    session.close()

if __name__ == "__main__":
    main()
