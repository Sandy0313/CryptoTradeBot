from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class Trade(Base):
    __tablename__ = 'trade_records'
    
    id = Column(Integer, primary_key=True)
    trading_symbol = Column(String)
    traded_quantity = Column(Integer)
    trade_price = Column(Float)
    trade_timestamp = Column(DateTime)

db_url = os.getenv('DATABASE_URL') 
engine = create_engine(db_url)

Base.metadata.create_all(engine)

SessionFactory = sessionmaker(bind=engine)
session = SessionFactory()