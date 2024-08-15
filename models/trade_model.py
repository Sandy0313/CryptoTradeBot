from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class Trade(Base):
    __tablename__ = 'trades'
    
    trade_id = Column(Integer, primary_key=True)
    symbol = Column(String)
    quantity = Column(Integer)
    price = Column(Float)
    timestamp = Column(DateTime)

engine = create_engine(os.getenv('DATABASE_URL')) 

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()