from typing import Optional
from datetime import date as date_type
from sqlalchemy.orm import Session

from models import WeatherRecord
from schemas import WeatherCreateRequest, WeatherUpdateRequest
from weather_service import geocode_location, fetch_weather


def create_weather_record(db: Session, request: WeatherCreateRequest) -> WeatherRecord:
    geo = geocode_location(request.location)

    existing = db.query(WeatherRecord).filter(
        WeatherRecord.resolved_name == geo["resolved_name"],
        WeatherRecord.start_date == request.start_date,
        WeatherRecord.end_date == request.end_date
    ).first()

    if existing:
        return existing

    weather_data = fetch_weather(
        geo["latitude"], geo["longitude"], request.start_date, request.end_date
    )

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
    db.refresh(record)

    return record


def get_weather_records(
    db: Session,
    page: int = 1,
    limit: int = 10,
    location: Optional[str] = None,
    start_date: Optional[date_type] = None,
    end_date: Optional[date_type] = None
):
    query = db.query(WeatherRecord)

    if location:
        query = query.filter(WeatherRecord.resolved_name.ilike(f"%{location}%"))

    if start_date:
        query = query.filter(WeatherRecord.start_date >= start_date)

    if end_date:
        query = query.filter(WeatherRecord.end_date <= end_date)

    total = query.count()

    offset = (page - 1) * limit
    records = query.order_by(WeatherRecord.created_at.desc()).offset(offset).limit(limit).all()

    return records, total


def get_weather_record_by_id(db: Session, record_id: int):
    return db.query(WeatherRecord).filter(WeatherRecord.id == record_id).first()


def update_weather_record(db: Session, record_id: int, request: WeatherUpdateRequest):
    record = db.query(WeatherRecord).filter(WeatherRecord.id == record_id).first()

    if not record:
        return None

    new_start = request.start_date or record.start_date
    new_end = request.end_date or record.end_date

    if new_end < new_start:
        raise ValueError("end_date must be on or after start_date")

    weather_data = fetch_weather(
        float(record.latitude), float(record.longitude), new_start, new_end
    )

    record.start_date = new_start
    record.end_date = new_end
    record.weather_data = weather_data

    db.commit()
    db.refresh(record)

    return record


def delete_weather_record(db: Session, record_id: int) -> bool:
    record = db.query(WeatherRecord).filter(WeatherRecord.id == record_id).first()

    if not record:
        return False

    db.delete(record)
    db.commit()

    return True