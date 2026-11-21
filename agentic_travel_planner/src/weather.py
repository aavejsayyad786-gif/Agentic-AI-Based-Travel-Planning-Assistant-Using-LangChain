import requests
from langchain_core.tools import tool

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

def fetch_weather(city: str, days: int = 7) -> dict:
    """Fetch daily weather forecast for a city using the free Open-Meteo APIs."""
    geo = requests.get(GEOCODING_URL, params={"name": city, "count": 1, "language": "en", "format": "json"}, timeout=20)
    geo.raise_for_status()
    results = geo.json().get("results", [])
    if not results:
        raise ValueError(f"Could not find coordinates for {city}.")
    place = results[0]
    params = {
        "latitude": place["latitude"], "longitude": place["longitude"],
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "timezone": "auto", "forecast_days": min(max(int(days), 1), 7)
    }
    response = requests.get(FORECAST_URL, params=params, timeout=20)
    response.raise_for_status()
    payload = response.json()
    return {"location": place.get("name", city), "country": place.get("country", ""),
            "timezone": payload.get("timezone"), "daily": payload.get("daily", {})}

@tool
def get_weather_forecast(city: str, days: int = 7) -> str:
    """Get a live daily weather forecast for a city from Open-Meteo. No API key is needed."""
    import json
    try:
        return json.dumps(fetch_weather(city, days), ensure_ascii=False)
    except Exception as exc:
        return f"Weather lookup unavailable: {exc}. Do not invent weather values."
