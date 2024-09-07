
# **Fitness Tracker Application**

A Flask-based web application for tracking workouts and monitoring fitness progress. Users can log their daily workouts, view their workout history, and track their improvements over time.

## **Features**

- User Registration and Authentication
- Logging workouts with exercises, sets, repetitions, weight, and duration
- Viewing workout history and progress
- Responsive UI with HTML, CSS, and Flask templates

## **Tech Stack**

- **Backend**: Flask (Python), SQLAlchemy
- **Frontend**: HTML, CSS
- **Database**: SQLite (or any SQL database)
- **Authentication**: Password hashing with bcrypt

---

## **Installation**

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/fitness-tracker-app.git
cd fitness-tracker-app
```

### 2. Create a Virtual Environment and Activate It

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up the Database

Create the SQLite database and tables by running the following commands:

```bash
python
>>> from models import Base, engine
>>> Base.metadata.create_all(engine)
```

### 5. Run the Application

Start the Flask server:

```bash
python app.py
```

The app will be running at `http://127.0.0.1:5000/`.

---

## **File Structure**

```
fitness_tracker/
├── app.py                   # Flask app entry point
├── database.py              # Database connection setup (SQLAlchemy)
├── models.py                # Database models for Users, Exercises, Workouts
├── utils.py                 # Utility functions for password hashing
├── templates/               # HTML templates for rendering pages
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── log_workout.html
│   └── view_progress.html
├── static/                  # Static files (CSS)
│   └── styles.css
└── requirements.txt         # Python dependencies
```

---

## **Usage**

1. **Register a New Account**  
   Go to `/register` to create a new user account.

2. **Log In**  
   Use your credentials to log in at `/`.

3. **Dashboard**  
   Once logged in, you can navigate to your dashboard and access options like logging a workout or viewing your workout history.

4. **Log a Workout**  
   Go to `/log_workout` and fill out the form with your workout details, including exercises, sets, reps, weight, duration, and distance.

5. **View Progress**  
   Head over to `/view_progress` to see a summary of your previous workouts and track your fitness progress over time.

---

## **Future Enhancements**

- Add charts for data visualization (e.g., tracking weight progress, reps, or total time over time)
- Enable users to set fitness goals and track achievement rates
- Add mobile-responsive design

---

## **License**

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## **Contributing**

Feel free to fork this project and submit pull requests. Contributions are welcome!

