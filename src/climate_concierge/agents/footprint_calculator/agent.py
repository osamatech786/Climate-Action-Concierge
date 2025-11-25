from google.adk.agents import Agent
from climate_concierge.tools import get_uk_carbon_intensity

root_agent = Agent(
    name="footprint_calculator",
    model="gemini-2.5-flash",
    instruction="""Calculate UK carbon footprint precisely using code execution.

Extract from user: car_miles, electricity_kwh, gas_kwh, postcode, diet type.
Use get_uk_carbon_intensity(postcode) for live grid data.

Calculate (2025 UK factors):
- Transport: car_miles * 0.207 / 1000 tons
- Electricity: electricity_kwh * grid_intensity / 1000000 tons
- Gas: gas_kwh * 0.183 / 1000 tons
- Diet: 365 * 1.2 / 1000 tons (meat-heavy)

Return breakdown: Transport X.XX tons, Electricity X.XX tons (at Xg/kWh), Gas X.XX tons, Diet X.XX tons, Total X.XX tons.""",
    description="Calculates carbon footprint with live UK grid data",
    tools=[get_uk_carbon_intensity]
)
