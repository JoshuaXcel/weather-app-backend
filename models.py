from sqlalchemy import Column, Integer, String, Date, JSON, DateTime
from sqlalchemy.sql import func
from database import Base

class WeatherRecord(Base):
    __tablename__ = "weather_records"

    id = Column(Integer, primary_key=True, index=True) #Auto-incrementing ID

    location_input = Column(String, nullable=False) #Raw text user typed, e.g. "Abuja"
    resolved_name = Column(String, nullable=False) #Confirmed name from geocoding, e.g. "Abuja, Nigeria"

    latitude = Column(String, nullable=False) #Stored as string to avoid float precision issues
    longitude = Column(String, nullable=False) #Stored as string for the same reason above

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    weather_data = Column(JSON, nullable=False) #List of daily temps: [{"date": ..., "temp_max": ..., "temp_min": ...}, ...]

    created_at = Column(DateTime(timezone=True), server_default=func.now()) #Auto-set on creation
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()) #Auto-updated on edit