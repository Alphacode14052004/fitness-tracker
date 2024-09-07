from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database connection (replace with your actual database URL)
DATABASE_URL = 'sqlite:///fitness_tracker.db'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
