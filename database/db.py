from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConfig:
    
    def __init__(self):
        self.DATABASE_URL = self.get_database_url()
        self.engine = self.create_engine_instance()
        self.SessionLocal = self.create_session_factory()

    @staticmethod
    def get_database_url():
        return os.getenv("DATABASE_URL")

    def create_engine_instance(self):
        return create_engine(self.DATABASE_URL)

    def create_session_factory(self):
        return sessionmaker(autocommit=False, autoflush=False, bind=self.engine)


database_config = DatabaseConfig()

def get_db():
    db = database_config.SessionLocal()
    try:
        yield db
    finally:
        db.close()