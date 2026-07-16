# Weather App API

A FastAPI backend that lets users fetch, store, and manage historical weather data for any location, with full CRUD, data export, and location mapping.

**Developer:** Joshua Mudana

**About PM Accelerator:** Product Manager Accelerator (PM Accelerator) offer training, education, and job opportunities for Product Managers, creating room for constant improvement and shaping the next generation of PMs. Whether you're a newbie or you've spent years in the industry, you're guaranteed to find a new opportunity with the help of PM Accelerator.

## Features

- **Create**: Submit a location (city, town, landmark, etc.) and a date range to fetch and store daily temperature data
- **Read**: List all saved records with pagination and filtering (by location or date range), or fetch a single record by ID
- **Update**: Change the date range on an existing record (re-fetches weather data for the new range)
- **Delete**: Remove a record
- **Validation**: Rejects invalid date ranges (end before start) and unresolvable locations (via geocoding)
- **Caching**: Repeated requests for the same location + date range return the cached record instead of re-fetching from the weather API
- **Export**: Download any record as JSON, CSV, or XML
- **Location map**: Get an OpenStreetMap embed/view link for any saved record's location
- **Logging**: All creates, updates, deletes, and errors are logged
- **Health check**: `GET /health`

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL + SQLAlchemy ORM
- **Weather data**: [Open-Meteo](https://open-meteo.com/) (free, no API key required)
- **Geocoding**: Open-Meteo Geocoding API (free, no API key required)
- **Maps**: OpenStreetMap (free, no API key required)

## Setup

### Prerequisites
- Python 3.12+
- PostgreSQL running locally (or accessible via connection string)

### Steps

1. Clone the repo:
```bash
   git clone https://github.com/JoshuaXcel/weather-app-backend.git
   cd weather-app-backend
```

2. Create and activate a virtual environment:
```bash
   python3 -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
   pip install -r requirements.txt
```

4. Set up your database:
```sql
   CREATE USER weatherapp_user WITH PASSWORD 'your_password';
   CREATE DATABASE weatherapp OWNER weatherapp_user;
```

5. Copy `.env.example` to `.env` and fill in your database credentials:
```bash
   cp .env.example .env
```
   Then edit `.env`:

DATABASE_URL=postgresql://weatherapp_user:your_password@localhost:5432/weatherapp
Note: if your password contains special characters (e.g. `#`), URL-encode them (e.g. `#` becomes `%23`).

6. Run the app:
```bash
   uvicorn main:app --reload
```

7. Open your browser to `http://127.0.0.1:8000/docs` for interactive API documentation.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | App info + developer/PM Accelerator description |
| GET | `/health` | Health check |
| POST | `/weather/` | Create a weather record (location + date range) |
| GET | `/weather/` | List records (supports `page`, `limit`, `location`, `start_date`, `end_date` query params) |
| GET | `/weather/{id}` | Get a single record |
| PUT | `/weather/{id}` | Update a record's date range |
| DELETE | `/weather/{id}` | Delete a record |
| GET | `/weather/{id}/export?format=json\|csv\|xml` | Export a record |
| GET | `/weather/{id}/map` | Get an OpenStreetMap link for the record's location |

## Example: Creating a record

```bash
curl -X POST "http://127.0.0.1:8000/weather/" \
  -H "Content-Type: application/json" \
  -d '{"location": "Akure", "start_date": "2026-07-01", "end_date": "2026-07-05"}'
```

## Notes

- Location validation is handled via the Open-Meteo Geocoding API — if a location can't be resolved, the API returns a 422 error.
- Date range validation ensures `end_date` is never before `start_date`.
- Weather data storage uses caching: identical location + date range requests return the existing record rather than hitting the external API again.