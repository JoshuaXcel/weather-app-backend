import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv() #Loading variables from .env file

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file")

engine = create_engine(DATABASE_URL) #Connection to Postgres

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #Each request gets its own session

Base = declarative_base() #All models will inherit from base model

def get_db():
    #Dependency that provides a DB session and closes it after use
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()