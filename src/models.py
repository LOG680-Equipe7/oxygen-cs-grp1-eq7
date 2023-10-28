from sqlalchemy import Column, Integer, String, Sequence, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class TemperatureLog(Base):
    __tablename__ = 'temperature_log'
    id = Column(Integer, Sequence('temp_log_id_seq'), primary_key=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    temperature = Column(Float)
    action = Column(String(50))
