from sqlalchemy import Column, String, Numeric, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class WeatherStage(Base):
    __tablename__ = "weather_stg"
    
    city = Column(String(50), primary_key=True)
    latitude = Column(Numeric(6, 4))
    longitude = Column(Numeric(7, 4))
    reading_timestamp = Column(DateTime, primary_key=True)
    temperature_celsius = Column(Numeric(4, 1))
    relative_humidity = Column(Numeric(3, 0))
    wind_speed_kmh = Column(Numeric(4, 1))
    extracted_at = Column(DateTime, server_default=func.now())
