import streamlit as st
from src.agent import create_travel_agent, run_travel_agent
from src.data_tools import load_all_data
from src.itinerary import build_fallback_plan
from src.weather import get_weather_forecast
from src.utils import parse_json_from_text

st.set_page_config(page_title="AI Travel Planning Assistant", page_icon="✈️", layout="wide")
st.title("✈️ Agentic AI-Based Travel Planning Assistant")
st.caption("LangChain tool-calling agent • Flight, hotel, attractions, weather and budget planning")

with st.sidebar:
    st.header("Trip preferences")
    origin = st.text_input("Departure city", "Pune")
    destination = st.text_input("Destination city", "Goa")
    start_date = st.date_input("Start date")
    days = st.slider("Trip duration (days)", 3, 7, 3)
    travelers = st.number_input("Number of travelers", min_value=1, max_value=12, value=1)
    budget = st.number_input("Total budget (₹)", min_value=1000, value=20000, step=1000)
    priorities = st.multiselect("What matters most?", ["Lowest cost", "Fastest flight", "Highly rated hotel", "Nature", "Beaches", "History", "Food", "Family friendly"], default=["Lowest cost", "Highly rated hotel"])
    extra = st.text_area("Additional preferences", "Prefer comfortable stays and a balanced sightseeing schedule.")
    make_plan = st.button("Generate my trip plan", type="primary", use_container_width=True)

st.info("Dataset note: flight, hotel and attraction suggestions are from the included sample JSON files. They are demonstration data, not live inventory or bookable prices. Weather is fetched from Open-Meteo when internet access is available.")

if make_plan:
    if not origin.strip() or not destination.strip():
        st.error("Please enter both departure and destination cities.")
        st.stop()
    request = f"""Plan a {days}-day trip from {origin} to {destination}, starting {start_date.isoformat()},
    for {travelers} traveler(s), with a total budget of INR {budget}.
    Priorities: {', '.join(priorities) if priorities else 'balanced'}. Additional preferences: {extra}.
    Use the available tools. Do not claim anything is booked. Clearly distinguish sample dataset estimates
    from live weather data. Return a practical day-wise itinerary and an itemized budget."""
    with st.spinner("The travel agent is checking flights, stays, attractions and weather..."):
        try:
            agent = create_travel_agent()
            answer = run_travel_agent(agent, request)
            st.markdown(answer)
        except Exception as e:
            st.warning(f"Agent execution could not complete ({e}). Showing a local planning result instead.")
            data = load_all_data()
            plan = build_fallback_plan(origin, destination, days, travelers, budget, data)
            st.markdown(plan)
            st.caption("Fallback mode uses local JSON datasets. Add a valid OPENAI_API_KEY to enable the LangChain tool-calling agent.")

st.divider()
st.subheader("Project modules")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Planning tools", "5")
c2.metric("Itinerary length", "3–7 days")
c3.metric("Weather source", "Open-Meteo")
c4.metric("Interface", "Streamlit")
with st.expander("How this project works"):
    st.markdown("""
    1. Streamlit collects trip preferences.
    2. A LangChain tool-calling agent decides which planning tools to use.
    3. Tools search the included `flights.json`, `hotels.json`, and `places.json` files.
    4. The weather tool calls Open-Meteo (no API key required).
    5. The agent combines the results into a day-wise itinerary and estimated budget.
    """)
