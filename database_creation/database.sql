-- Create Users Table
CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Exercises Table
CREATE TABLE Exercises (
    exercise_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50), -- e.g., Strength, Cardio, Flexibility
    description TEXT
);

-- Create Workout_Sessions Table
CREATE TABLE Workout_Sessions (
    session_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id),
    session_date DATE NOT NULL,
    notes TEXT
);

-- Create Workout_Details Table
CREATE TABLE Workout_Details (
    detail_id SERIAL PRIMARY KEY,
    session_id INT REFERENCES Workout_Sessions(session_id) ON DELETE CASCADE,
    exercise_id INT REFERENCES Exercises(exercise_id),
    sets INT,
    repetitions INT,
    weight DECIMAL(5,2), -- in kilograms or pounds
    duration INT, -- in seconds
    distance DECIMAL(5,2) -- for cardio exercises, in kilometers or miles
);
