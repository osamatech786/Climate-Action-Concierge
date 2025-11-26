from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name="footprint_calculator",
    model="gemini-2.5-flash",
    instruction="""Calculate UK carbon footprint with grid data.

1. Extract: car_miles, car_type (petrol/diesel), electricity_kwh, heating_fuel (gas/oil), heating_kwh, postcode, diet

2. Use google_search for grid intensity:
   Search: "UK carbon intensity [postcode] average gCO2/kWh site:carbon-intensity.org.uk"
   Typical: London ~103 g/kWh, Scotland ~89 g/kWh, UK ~141 g/kWh

3. Calculate:
   - transport:
     * petrol: car_miles * 0.207 / 1000 tons
     * diesel: car_miles * 0.125 / 1000 tons (more efficient)
     * if not specified: use 0.207 (avg)
   - electricity = electricity_kwh * grid_intensity / 1000000 tons
   - heating:
     * gas: heating_kwh * 0.183 / 1000 tons
     * oil: heating_kwh * 0.27 / 1000 tons
   - diet:
     * red meat (beef/lamb) most days: 1.8 tons
     * meat daily: 0.44 tons
     * chicken daily: 0.24 tons
     * vegetarian: 0.18 tons

4. Output:
   Transport: X.XX tons
   Electricity: X.XX tons (at Xg/kWh average)
   [Gas/Heating Oil]: X.XX tons
   Diet: X.XX tons
   Total: X.XX tons

Use "average" for consistency.""",
    description="Calculates carbon footprint with live UK grid data",
    tools=[google_search]
)
