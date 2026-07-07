from fastapi import FastAPI
from database import engine, Base
import models #Importing this so that SQLAlchemy knows about WeatherRecord before creating tables
from routers import weather

Base.metadata.create_all(bind=engine) #Creating all tables that don't already exist

app = FastAPI(title="Weather App API")
app.include_router(weather.router)

@app.get("/")
def root():
    #Root endpoint with app info...
    return {
        "app": "Weather App API",
        "developer": "Joshua Mudana", 
        "about": "Product Manager Accelerator (PM Accelerator) offer training, education, and job opportunities "
                  "for Product Managers, creating room for constant improvement and shaping the next generation of PMs. "
                  "Whether you’re a newbie or you’ve spent years in the industry, you’re"
                  "guaranteed to find a new opportunity with the help of PM Accelerator." 
                  #From PMA about at https://www.pmaccelerator.io/about-us
    } 

@app.get("/health")
def health_check():
    return {"status": "ok"}