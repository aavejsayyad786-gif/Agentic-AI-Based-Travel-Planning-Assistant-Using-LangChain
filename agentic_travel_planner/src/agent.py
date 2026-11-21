from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from .config import OPENAI_API_KEY, OPENAI_MODEL
from .data_tools import search_flights, recommend_hotels, discover_places, estimate_trip_budget
from .weather import get_weather_forecast

TOOLS = [search_flights, recommend_hotels, discover_places, get_weather_forecast, estimate_trip_budget]

def create_travel_agent():
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is missing. Add it to your .env file.")
    llm = ChatOpenAI(model=OPENAI_MODEL, temperature=0.2, api_key=OPENAI_API_KEY)
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a careful AI travel-planning assistant. Use tools to retrieve flights, hotels,
        attractions, weather and budget data. You can create a 3–7 day itinerary. Never say anything is booked.
        The flight, hotel and attraction tools use a small illustrative JSON dataset, not live inventory.
        Weather comes from Open-Meteo and may fail. Never invent unavailable data. State assumptions,
        currency INR, price basis (per person/per room/night), and explain why options were selected.
        Keep the schedule geographically sensible and do not overload each day. Show trip summary, selected
        flight, hotel, day-wise plan, weather by day if available, budget breakdown and reasoning."""),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ])
    agent = create_tool_calling_agent(llm, TOOLS, prompt)
    return AgentExecutor(agent=agent, tools=TOOLS, verbose=True, max_iterations=12, handle_parsing_errors=True)

def run_travel_agent(agent, request: str) -> str:
    result = agent.invoke({"input": request})
    return result.get("output", "The agent did not return an answer.")
