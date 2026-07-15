import logging
from typing import Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas import (
    WeatherCreateRequest,
    WeatherUpdateRequest,
    WeatherRecordResponse,
    PaginatedWeatherResponse
)
import crud

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/weather", tags=["weather"])


@router.post("/", response_model=WeatherRecordResponse)
def create_weather(request: WeatherCreateRequest, db: Session = Depends(get_db)):
    try:
        record = crud.create_weather_record(db, request)
        logger.info(f"Weather record created/retrieved for '{request.location}'")
        return record
    except ValueError as e:
        logger.error(f"Validation error for '{request.location}': {e}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error for '{request.location}': {e}")
        raise HTTPException(status_code=503, detail="Weather service temporarily unavailable")


@router.get("/", response_model=PaginatedWeatherResponse)
def list_weather(
    page: int = 1,
    limit: int = 10,
    location: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    records, total = crud.get_weather_records(db, page, limit, location, start_date, end_date)
    return {"total": total, "page": page, "limit": limit, "results": records}


@router.get("/{record_id}", response_model=WeatherRecordResponse)
def get_weather(record_id: int, db: Session = Depends(get_db)):
    record = crud.get_weather_record_by_id(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"Weather record {record_id} not found")
    return record


@router.put("/{record_id}", response_model=WeatherRecordResponse)
def update_weather(record_id: int, request: WeatherUpdateRequest, db: Session = Depends(get_db)):
    try:
        record = crud.update_weather_record(db, record_id, request)
        if not record:
            raise HTTPException(status_code=404, detail=f"Weather record {record_id} not found")
        logger.info(f"Weather record {record_id} updated")
        return record
    except ValueError as e:
        logger.error(f"Validation error updating {record_id}: {e}")
        raise HTTPException(status_code=422, detail=str(e))


@router.delete("/{record_id}")
def delete_weather(record_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_weather_record(db, record_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Weather record {record_id} not found")
    logger.info(f"Weather record {record_id} deleted")
    return {"message": f"Weather record {record_id} deleted successfully"}