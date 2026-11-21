# Project Report
## Project Title
Agentic AI-Based Travel Planning Assistant Using LangChain

## Domain
Travel / Tourism

## 1. Problem Statement
Planning a trip requires choosing flights, hotels and attractions while considering time, budget, weather, distance and personal preferences. Travelers often switch between multiple websites, compare inconsistent information and manually build itineraries that may be inefficient, unrealistic or incomplete. This project provides an intelligent assistant that combines travel data and weather information to generate a structured itinerary.

## 2. Business Use Cases
Travel agencies, hotel platforms, airline aggregators and tourism companies can use conversational travel-planning tools to reduce support workload, provide personalized recommendations, automate itinerary design, improve customer satisfaction, and save users time.

## 3. Objectives
- Build an agentic AI system using LangChain to create trip itineraries.
- Integrate flight, hotel and places searches using JSON datasets.
- Integrate real-time weather using the free Open-Meteo API.
- Enable multi-step tool use and decision-making through a LangChain tool-calling agent.
- Generate day-wise itinerary, accommodation suggestion, weather expectations and budget estimate.
- Apply filtering and ranking such as cheapest flight and highest-rated hotel.
- Explain recommendation choices.
- Provide a Streamlit interface and readable output.

## 4. System Approach
### Step 1 — Data Setup
The project includes `flights.json`, `hotels.json` and `places.json` as demonstration datasets. Open-Meteo provides weather forecasts through its public API.

### Step 2 — Build Tools
- Flight Search Tool: filters origin and destination; ranks by price or duration.
- Hotel Recommendation Tool: filters by city, nightly price and rating.
- Places Discovery Tool: filters by city and category; ranks by rating.
- Weather Lookup Tool: geocodes a city and fetches daily forecast.
- Budget Estimation Tool: adds flight, hotel and food/local travel estimates.

### Step 3 — Create the Agent
A LangChain tool-calling agent interprets the request, chooses tools, retrieves information, reasons over the results, and prepares a 3–7 day itinerary and cost estimate.

### Step 4 — Generate Output
The app presents trip summary, flight option, hotel recommendation, day-wise itinerary, weather when available, budget breakdown and selection rationale.

## 5. Expected Results
The system is expected to create a clear trip plan containing a flight suggestion, hotel suggestion, attractions arranged by day, weather forecast when available, and an estimated total budget.

## 6. Technology Stack
- Python
- LangChain and LangChain OpenAI integration
- Streamlit
- JSON datasets
- Requests / Open-Meteo API
- python-dotenv

## 7. Limitations
- Bundled travel JSON data is illustrative and limited; it is not live booking inventory.
- Flight and hotel prices are sample estimates and must be verified before travel.
- The application does not make reservations or payments.
- LLM agent functionality requires a valid OpenAI API key and may incur API usage charges.
- Weather availability depends on Open-Meteo forecast coverage and network access.

## 8. Conclusion
The project demonstrates how an agentic AI workflow can combine structured datasets, external weather information and multi-step tool calling to assist with travel planning. Its modular tools and Streamlit interface provide a foundation that can later be connected to verified travel supplier APIs.
