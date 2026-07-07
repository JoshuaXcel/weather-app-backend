from pydantic import BaseModel, field_validator
from datetime import date, datetime
from typing import List, Optional


class WeatherCreateRequest(BaseModel):
    location: str
    start_date: date
    end_date: date

    @field_validator("end_date")
    @classmethod
    def validate_date_range(cls, end_date, info):
        start_date = info.data.get("start_date")
        if start_date and end_date < start_date:
            raise ValueError("end_date must be on or after start_date") #Catches reversed date ranges
        return end_date


class DailyTemp(BaseModel):
    date: str
    temp_max: float
    temp_min: float


class WeatherRecordResponse(BaseModel):
    id: int
    location_input: str
    resolved_name: str
    latitude: str
    longitude: str
    start_date: date
    end_date: date
    weather_data: List[DailyTemp]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True #Allows Pydantic to read directly from SQLAlchemy model objects