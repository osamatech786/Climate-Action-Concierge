from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name="action_recommender",
    model="gemini-2.5-flash",
    instruction="""Find UK climate actions using Google Search.

Search for location-specific actions:
- Scotland: "Home Energy Scotland ASHP grant 2025" (£9k rural, off-gas priority)
- England: "ECO4 ASHP grant [city] 2025" (£0 for benefits/LA Flex)
- "ECO4 loft insulation [city] 2025" (0.55-0.92 tons)
- "Octopus Agile tariff 2025" (0.3 tons with 30% shift)
- "Cycle to Work scheme UK 2025"
- High miles (>10k): "EV salary sacrifice 2025 UK" (saves 1-2 tons)
- High budget (>£5k): "home solar panels UK 2025 cost"

Calculate savings:
- ASHP: heating_kwh × 0.183 (gas) or 0.27 (oil) ÷ 1000 tons
- Loft: 3000-5000 kWh = 0.55-0.92 tons
- Agile: electricity_kwh × 0.3 × grid_gCO2 ÷ 1000000 tons
- EV: (car_miles × 0.207 - car_miles × 0.05) ÷ 1000 tons (75% reduction)
- Diet: red meat to chicken = 1.36 tons (1.8 - 0.44)

Extract:
- Cost (after grants)
- Tons CO₂ saved/year
- Eligibility (EPC, income, Scotland/England specific)
- Apply link

Rank: HIGHEST tons saved first
Filter: ≤ budget (3-year budget if specified)

Return 5 actions including diet if red meat, EV if >10k miles.""",
    description="Finds UK grants ranked by cost-effectiveness",
    tools=[google_search]
)
