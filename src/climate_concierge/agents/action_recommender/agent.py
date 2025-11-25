from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name="action_recommender",
    model="gemini-2.5-flash",
    instruction="""Find UK climate actions using Google Search.

Search for:
- "ECO4 ASHP grant [city] 2025 eligibility" (saves 1.5-1.9 tons gas heating)
- "ECO4 loft insulation [city] 2025" (saves 0.55-1 ton from 3000-5000 kWh gas)
- "Octopus Agile tariff savings 2025" (saves 0.3-0.5 tons via off-peak green shift)
- "Cycle to Work scheme UK 2025" (saves full car emissions if replacing commute)
- "cavity wall insulation [city] cost 2025" (saves 0.4-0.7 tons)

Calculate realistic savings:
- ASHP: replaces gas heating (user's gas_kwh * 0.183 / 1000 tons)
- Loft: 3000-5000 kWh gas saved = 0.55-0.9 tons
- Agile: 10-15% electricity shift to green = user's elec tons * 0.1-0.15
- Cycle: miles replaced * 0.207 / 1000 tons

Extract: Cost (after grants), Tons saved, Eligibility, Apply link
Calculate: £/ton = cost / (tons * 10)
Rank: Free first, then lowest £/ton
Filter: ≤ budget

Return EXACTLY 5 actions with complete data.""",
    description="Finds UK grants ranked by cost-effectiveness",
    tools=[google_search]
)
