from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    
    def __init__(self):
        self.database_url = self._fetch_database_url()
        self.engine = self._initialize_engine()
        self.session_factory = self._configure_session_factory()

    @staticmethod
    def _fetch_database_url():
        return os.getenv("DATABASE_URL")

    def _initialize_engine(self):
        return create_engine(self.database_url)

    def _configure_session_factory(self):
        return sessionmaker(autocommit=False, autoflush=False, bind=self.engine)


database_manager = DatabaseManager()

def establish_db_session():
    db_session = database_manager.session_factory()
    try:
        yield db_session
    finally:
        db_session.close()