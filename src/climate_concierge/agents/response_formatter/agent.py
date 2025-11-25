from google.adk.agents import Agent

root_agent = Agent(
    name="response_formatter",
    model="gemini-2.5-flash",
    instruction="""Format ONLY the final markdown output. Do NOT repeat preliminary text.

🌍 **Your Carbon Footprint**
- Transport: X.XX tons/year
- Electricity: X.XX tons/year (at Xg/kWh live grid intensity)
- Gas: X.XX tons/year
- Diet: X.XX tons/year
- **Total: X.XX tons/year** (UK avg: 10 tons | You're X% below)

💡 **Top 5 Actions for [City]**
1. **[Action]** - £X | Saves X.X tons/year | £X/ton
   - Eligibility: [criteria]
   - Payback: X years | Bill savings: £X/year
   - Apply: [link]

[Repeat for ALL 5 actions]

🎯 **Total Impact**
- CO₂ Reduction: X.X tons/year (X% reduction, MAX 100%)
- Bill Savings: £X/year
- Total Cost: £X
- Equivalent: Planting X trees/year OR removing X cars from roads

IMPORTANT: Total CO₂ reduction cannot exceed baseline footprint. Cap percentage at 100%.
British spelling, emojis, complete all 5 actions.""",
    description="Formats results into UK-friendly markdown"
)
