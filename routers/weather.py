import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas import WeatherCreateRequest, WeatherRecordResponse
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
        #Covers both "location not found" and "weather API failed" cases
        logger.error(f"Validation error for '{request.location}': {e}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error for '{request.location}': {e}")
        raise HTTPException(status_code=503, detail="Weather service temporarily unavailable")