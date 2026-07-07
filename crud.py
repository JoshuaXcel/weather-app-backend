from sqlalchemy.orm import Session
from models import WeatherRecord
from schemas import WeatherCreateRequest
from weather_service import geocode_location, fetch_weather


def create_weather_record(db: Session, request: WeatherCreateRequest) -> WeatherRecord:
    #Check cache first: if same resolved location and date range is already stored
    geo = geocode_location(request.location) #Raises ValueError if location not found

    existing = db.query(WeatherRecord).filter(
        WeatherRecord.resolved_name == geo["resolved_name"],
        WeatherRecord.start_date == request.start_date,
        WeatherRecord.end_date == request.end_date
    ).first()

    if existing:
        return existing #Cache hit, skip the API call entirely

    weather_data = fetch_weather(
        geo["latitude"], geo["longitude"], request.start_date, request.end_date
    ) #Raises ValueError if weather API fails

    record = WeatherRecord(
        location_input=request.location,
        resolved_name=geo["resolved_name"],
        latitude=str(geo["latitude"]),
        longitude=str(geo["longitude"]),
        start_date=request.start_date,
        end_date=request.end_date,
        weather_data=weather_data
    )

    db.add(record)
    db.commit()
    db.refresh(record) #Pulls back the auto-generated id, created_at, etc.

    return record