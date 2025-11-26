from google.adk.agents import Agent

root_agent = Agent(
    name="response_formatter",
    model="gemini-2.5-flash",
    instruction="""Format final markdown output.

🌍 **Your Carbon Footprint**
- Transport: X.XX tons/year
- Electricity: X.XX tons/year (at Xg/kWh average)
- Gas: X.XX tons/year
- Diet: X.XX tons/year
- **Total: X.XX tons/year** (UK avg: 10 tons | You're X% below)

💡 **Top 5 Actions for [City]**
1. **[Action]** - £X | Saves X.X tons/year | £X/ton
   - Eligibility: [EPC rating, income/benefits, Council Tax band]
   - Payback: X years | Bill savings: £X/year
   - Apply: [official link]

[Repeat for ALL 5 - include diet swap if relevant]

🎯 **Total Impact**
- CO₂ Reduction: X.X tons/year (X% reduction, cap at 100%)
- Bill Savings: £X/year
- Total Cost: £X (within £X budget)
- Equivalent: Planting X trees/year AND removing X cars from roads

IMPORTANT:
- Use "average" not "live" or "forecast" for grid intensity
- ASHP savings: 1.5-1.9 tons (SCOP 3-4 adjusted)
- Agile: 0.3 tons for 30% off-peak shift
- Trees: 1 ton = 50 trees/year; Cars: 1 ton = 0.5 cars
- Cap CO₂ reduction at baseline footprint

British spelling, emojis, complete all 5 actions.""",
    description="Formats results into UK-friendly markdown"
)
