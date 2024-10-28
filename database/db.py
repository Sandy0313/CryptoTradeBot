from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve DATABASE_URL from the environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Create a SQL Alchemy engine instance
engine = create_engine(DATABASE_URL)

# Create a session factory bound to this engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Generator yielding a database session.

    Yields:
        db (Session): The SQLAlchemy session object.

    Ensures that the session is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()