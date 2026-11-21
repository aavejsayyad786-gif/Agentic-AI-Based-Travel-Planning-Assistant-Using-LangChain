# Agentic AI-Based Travel Planning Assistant Using LangChain

A Streamlit travel-planning app with a LangChain tool-calling agent. It searches local JSON datasets for flights, hotels and attractions, calls Open-Meteo for weather, estimates costs, and generates a 3–7 day itinerary.

## 1. Requirements
- Windows 10/11, macOS or Linux
- Python 3.10 or 3.11 recommended
- Internet connection for package installation and live weather
- OpenAI API key for the LLM-powered agent (usage may incur charges)

## 2. Setup on Windows
Open Command Prompt in this project folder:

```bat
py -3.11 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```

Open `.env` in VS Code and replace `your_openai_api_key_here` with your own API key. Never share or submit your real `.env` file.

## 3. Run
```bat
streamlit run app.py
```
A browser tab will open. Enter origin, destination, dates, duration, travelers, budget and preferences, then click **Generate my trip plan**.

Without an API key, the app still opens and uses a local-data fallback planner. The fallback does not call the LLM and does not fetch live weather.

## 4. Project structure
```text
agentic_travel_planner/
├── app.py
├── requirements.txt
├── .env.example
├── README.md
├── PROJECT_REPORT.md
├── data/
│   ├── flights.json
│   ├── hotels.json
│   └── places.json
├── src/
│   ├── __init__.py
│   ├── agent.py
│   ├── config.py
│   ├── data_tools.py
│   ├── itinerary.py
│   ├── utils.py
│   └── weather.py
└── tests/
    └── test_data.py
```

## 5. Tools implemented
1. `search_flights`: route filter and cheapest/fastest ranking.
2. `recommend_hotels`: city, maximum nightly price and minimum rating filters.
3. `discover_places`: city and attraction category filter.
4. `get_weather_forecast`: Open-Meteo geocoding + daily forecast, no API key.
5. `estimate_trip_budget`: flight + accommodation + daily food/local allowance.

The LangChain tool-calling agent chooses tools, gathers results and composes the itinerary. A local fallback keeps the UI usable if the LLM key or network is unavailable.

## 6. Data and accuracy limitations
The included JSON files are **small illustrative sample datasets** so the project runs immediately. They are not real-time flight/hotel inventory, verified rates, or booking integrations. The app does not book anything. For a real deployment, replace sample data with licensed supplier APIs and add validation for availability, taxes, baggage, cancellation terms and currency conversion.

Open-Meteo forecast coverage is limited to the available forecast horizon (up to 7 days in this implementation). Forecast availability depends on the requested date and API service.

## 7. Run tests
```bat
pytest -q
```

## 8. Troubleshooting
- `OPENAI_API_KEY is missing`: create `.env` from `.env.example` and add your key.
- `ModuleNotFoundError`: activate `.venv`, then run `pip install -r requirements.txt`.
- Weather lookup error: check internet connectivity; the app/agent should report the lookup failure rather than inventing weather.
- No flight/hotel/place results: edit the matching JSON file in `data/`; city and route names must match the user's input.
