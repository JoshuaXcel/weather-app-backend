import httpx
from datetime import date

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def geocode_location(query: str) -> dict:
    #Calls Open-Meteo geocoding API to turn a location string into lat/lon and resolved name
    params = {"name": query, "count": 1} #count=1 it grabs the single best match (fuzzy match handled by the API itself)

    response = httpx.get(GEOCODING_URL, params=params, timeout=10)
    response.raise_for_status() #Raises an exception if the API call itself fails (network, 500, etc.)

    data = response.json()

    if "results" not in data or len(data["results"]) == 0:
        raise ValueError(f"No location found matching '{query}'") 

    best_match = data["results"][0]

    return {
        "resolved_name": f"{best_match['name']}, {best_match.get('admin1', '')}, {best_match['country']}",
        "latitude": best_match["latitude"],
        "longitude": best_match["longitude"]
    }


def fetch_weather(latitude: float, longitude: float, start_date: date, end_date: date) -> list:
    #Calls Open-Meteo forecast/historical API for daily temps within a date range
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "daily": "temperature_2m_max,temperature_2m_min",
        "timezone": "auto"
    }

    response = httpx.get(WEATHER_URL, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    if "daily" not in data:
        raise ValueError("Weather API did not return expected data")

    daily = data["daily"]
    results = []

    for i in range(len(daily["time"])):
        results.append({
            "date": daily["time"][i],
            "temp_max": daily["temperature_2m_max"][i],
            "temp_min": daily["temperature_2m_min"][i]
        })

    return results