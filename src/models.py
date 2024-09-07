from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, Text
from sqlalchemy.orm import relationship
from database import engine, Base

class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)

    workout_sessions = relationship('WorkoutSession', back_populates='user')

class Exercise(Base):
    __tablename__ = 'exercises'
    
    exercise_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

class WorkoutSession(Base):
    __tablename__ = 'workout_sessions'
    
    session_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    session_date = Column(Date)
    notes = Column(Text)

    user = relationship('User', back_populates='workout_sessions')
    details = relationship('WorkoutDetail', back_populates='workout_session')

class WorkoutDetail(Base):
    __tablename__ = 'workout_details'
    
    detail_id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey('workout_sessions.session_id'))
    exercise_id = Column(Integer, ForeignKey('exercises.exercise_id'))
    sets = Column(Integer)
    repetitions = Column(Integer)
    weight = Column(Float)
    duration = Column(Float)
    distance = Column(Float)

    workout_session = relationship('WorkoutSession', back_populates='details')
    exercise = relationship('Exercise')

Base.metadata.create_all(bind=engine)
