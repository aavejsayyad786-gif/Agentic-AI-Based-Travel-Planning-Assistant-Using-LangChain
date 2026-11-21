import json
import os
from typing import Any
from langchain_core.tools import tool
from .config import DATA_DIR

def _load(filename: str) -> list[dict[str, Any]]:
    path = os.path.join(DATA_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_all_data():
    return {
        "flights": _load("flights.json"),
        "hotels": _load("hotels.json"),
        "places": _load("places.json"),
    }

@tool
def search_flights(origin: str, destination: str, preference: str = "cheapest") -> str:
    """Search the local sample flight dataset by origin and destination. Preference can be cheapest or fastest."""
    rows = _load("flights.json")
    matches = [x for x in rows if x["origin"].lower() == origin.lower() and x["destination"].lower() == destination.lower()]
    if not matches:
        return f"No sample flights found for {origin} to {destination}. Explain that this is a limited demonstration dataset."
    key = "price_inr" if preference.lower() != "fastest" else "duration_hours"
    matches.sort(key=lambda x: x[key])
    return json.dumps(matches[:5], ensure_ascii=False)

@tool
def recommend_hotels(city: str, max_price_per_night: int = 10000, minimum_rating: float = 0) -> str:
    """Find sample hotels in a city, filtered by maximum nightly price and minimum rating; sort by rating."""
    rows = _load("hotels.json")
    matches = [x for x in rows if x["city"].lower() == city.lower()
               and x["price_per_night_inr"] <= max_price_per_night and x["rating"] >= minimum_rating]
    matches.sort(key=lambda x: (-x["rating"], x["price_per_night_inr"]))
    return json.dumps(matches[:8], ensure_ascii=False) if matches else f"No sample hotels match the filters in {city}."

@tool
def discover_places(city: str, category: str = "all") -> str:
    """Find sample attractions in a city. Category can be all, beach, nature, history, food, or culture."""
    rows = _load("places.json")
    matches = [x for x in rows if x["city"].lower() == city.lower()
               and (category.lower() == "all" or x["category"].lower() == category.lower())]
    matches.sort(key=lambda x: -x["rating"])
    return json.dumps(matches[:15], ensure_ascii=False) if matches else f"No sample attractions found for {city}."

@tool
def estimate_trip_budget(flight_cost_inr: int, hotel_per_night_inr: int, nights: int,
                         daily_food_local_inr: int, travelers: int = 1) -> str:
    """Estimate total trip cost in INR from flight, hotel, and daily food/local expenses."""
    flight = flight_cost_inr * travelers
    hotel = hotel_per_night_inr * nights
    local = daily_food_local_inr * nights * travelers
    total = flight + hotel + local
    return json.dumps({"currency": "INR", "flight_total": flight, "hotel_total": hotel,
                       "food_and_local_total": local, "estimated_total": total}, ensure_ascii=False)
