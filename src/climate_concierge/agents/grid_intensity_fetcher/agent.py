from google.adk.agents import Agent
from climate_concierge.tools import get_uk_carbon_intensity

root_agent = Agent(
    name="grid_intensity_fetcher",
    model="gemini-2.5-flash",
    instruction="""You ONLY fetch UK grid carbon intensity. 

When given a postcode, ALWAYS call get_uk_carbon_intensity(postcode) and return ONLY the gCO2_per_kWh value as a number.

Example: If postcode is "E17", call get_uk_carbon_intensity("E17") and return just the number like "103".""",
    description="Fetches live UK grid carbon intensity by postcode",
    tools=[get_uk_carbon_intensity]
)
