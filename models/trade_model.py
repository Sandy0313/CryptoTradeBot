from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base class for SQLAlchemy models
BaseModel = declarative_base()

class TradeRecord(BaseModel):
    __tablename__ = 'trades'
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    quantity = Column(Integer)
    price = Column(Float)
    timestamp = Column(DateTime)

# Initialize database connection
database_url = os.getenv('DATABASE_URL') 
engine = create_engine(database_url)

# Create database tables based on models
BaseModel.metadata.create_all(engine)

# Set up session factory for database transactions
DatabaseSession = sessionmaker(bind=engine)
db_session = DatabaseSession()