-- Insert Sample Users
INSERT INTO Users (username, email, password_hash)
VALUES
('john_doe', 'john@example.com', 'hashed_password1'),
('jane_smith', 'jane@example.com', 'hashed_password2');

-- Insert Sample Exercises
INSERT INTO Exercises (name, category, description)
VALUES
('Bench Press', 'Strength', 'Chest exercise using a barbell'),
('Running', 'Cardio', 'Outdoor running'),
('Squats', 'Strength', 'Lower body exercise using body weight or weights'),
('Yoga', 'Flexibility', 'Various stretching and breathing exercises');

-- Insert Sample Workout Sessions
INSERT INTO Workout_Sessions (user_id, session_date, notes)
VALUES
(1, '2024-04-01', 'Felt strong today'),
(2, '2024-04-02', 'Need to improve endurance');

-- Insert Sample Workout Details
INSERT INTO Workout_Details (session_id, exercise_id, sets, repetitions, weight, duration, distance)
VALUES
(1, 1, 4, 10, 80.0, NULL, NULL),
(1, 3, 3, 15, 60.0, NULL, NULL),
(2, 2, NULL, NULL, NULL, 1800, 5.0),
(2, 4, NULL, NULL, NULL, 3600, NULL);
