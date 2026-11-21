from .utils import money

def build_fallback_plan(origin, destination, days, travelers, budget, data):
    flights = [x for x in data["flights"] if x["origin"].lower() == origin.lower()
               and x["destination"].lower() == destination.lower()]
    hotels = [x for x in data["hotels"] if x["city"].lower() == destination.lower()]
    places = [x for x in data["places"] if x["city"].lower() == destination.lower()]
    flights.sort(key=lambda x: x["price_inr"])
    hotels.sort(key=lambda x: (-x["rating"], x["price_per_night_inr"]))
    places.sort(key=lambda x: -x["rating"])
    lines = [f"## {days}-day trip: {origin} → {destination}", "",
             "**Important:** This is a sample-data estimate. No flight or hotel has been booked."]
    if flights:
        f = flights[0]
        lines += [f"### Flight option", f"- {f['airline']} — {money(f['price_inr'])} per traveler; {f['duration_hours']} hours."]
    else:
        lines += ["### Flight option", f"- No sample flight found for {origin} → {destination}. Add a matching route to `data/flights.json`."]
    if hotels:
        h = hotels[0]
        lines += ["### Hotel recommendation", f"- {h['name']} — {h['rating']}/5, {money(h['price_per_night_inr'])} per night."]
    else:
        lines += ["### Hotel recommendation", f"- No sample hotel found for {destination}. Add a city entry to `data/hotels.json`."]
    lines += ["### Day-wise itinerary"]
    for day in range(days):
        lines.append(f"**Day {day+1}:** " + (", ".join(p["name"] for p in places[day*2:day*2+2]) if places[day*2:day*2+2] else "Explore the destination at a relaxed pace; verify local opening times."))
    flight_cost = flights[0]["price_inr"] * travelers if flights else 0
    hotel_cost = hotels[0]["price_per_night_inr"] * max(days-1, 0) if hotels else 0
    local_cost = 1200 * days * travelers
    total = flight_cost + hotel_cost + local_cost
    lines += ["### Estimated budget", f"- Flight: {money(flight_cost)}",
              f"- Hotel ({max(days-1,0)} nights): {money(hotel_cost)}",
              f"- Food and local travel (planning allowance): {money(local_cost)}",
              f"- **Estimated total: {money(total)}**",
              f"- User budget: {money(budget)}",
              "", "### Notes", "- Prices and inventory in the JSON files are illustrative sample data, not live quotes.",
              "- Weather is not included in fallback mode; run the agent with internet access to retrieve Open-Meteo data."]
    return "\n".join(lines)
