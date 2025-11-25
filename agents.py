from google import genai
from google.genai import types

def get_climate_recommendations(client, user_message):
    """Multi-step workflow with proper tool usage."""
    
    # Step 1: Calculate footprint with code execution and live data
    footprint_instruction = """Calculate carbon footprint precisely using code execution:

1. Extract: car_miles, electricity_kwh, gas_kwh, postcode from user message
2. Execute Python code with 2025 UK emission factors:
```python
import requests

# Extract values from user input
car_miles = 5000  # extract from user
electricity_kwh = 3000
gas_kwh = 12000
postcode = "G1"  # extract from user

# Get live UK grid intensity for location
try:
    url = f"https://api.carbon-intensity.org.uk/regional/postcode/{postcode}"
    response = requests.get(url, timeout=5)
    grid_intensity = response.json()["data"][0]["data"][0]["intensity"]["forecast"]
except:
    grid_intensity = 141  # 2025 UK average gCO2/kWh

# Transport (2025 UK avg petrol/diesel)
transport_tons = (car_miles * 0.207) / 1000

# Energy (2025 factors)
electricity_tons = (electricity_kwh * grid_intensity) / 1000000  # gCO2 to tons
gas_tons = (gas_kwh * 0.183) / 1000  # 2025 UK gas factor
energy_tons = electricity_tons + gas_tons

# Diet (daily meat = 1.2 kg CO2/day avg)
diet_tons = (365 * 1.2) / 1000

total_tons = transport_tons + energy_tons + diet_tons
print(f"Transport: {transport_tons:.2f} tons")
print(f"Electricity: {electricity_tons:.2f} tons (at {grid_intensity}g/kWh)")
print(f"Gas: {gas_tons:.2f} tons")
print(f"Diet: {diet_tons:.2f} tons")
print(f"Total: {total_tons:.2f} tons/year")
print(f"UK average: 10 tons/year")
print(f"Reduction potential: {10 - total_tons:.2f} tons")
```

Return the calculated breakdown."""

    footprint_config = types.GenerateContentConfig(
        system_instruction=footprint_instruction,
        tools=[types.Tool(code_execution={})],
        temperature=0
    )
    
    footprint_response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=user_message,
        config=footprint_config
    )
    
    # Step 2: Search for UK grants and actions with precise calculations
    search_instruction = """Search for UK climate actions and grants:

1. Use google_search to find:
   - "ECO4 grant Glasgow 2025 eligibility income limit"
   - "Home Energy Scotland ASHP grant 2025"
   - "Octopus Agile tariff Glasgow savings"
   - "loft insulation cost Glasgow 2025"
   - "Cycle to Work scheme UK savings"

2. For each action, extract:
   - Exact cost (after grants)
   - Tons CO2 saved per year (be conservative)
   - Eligibility criteria (income, EPC rating, benefits)
   - Apply link (gov.uk or official site)
   - Payback period in years

3. Use code_execution to calculate:
   - £ per ton saved = cost / (tons_saved * 10 years)
   - Total potential savings if all actions taken
   - Bill savings per year

4. Rank by: Free first, then lowest £/ton

Return top 5 actions with verified data from search."""

    search_config = types.GenerateContentConfig(
        system_instruction=search_instruction,
        tools=[types.Tool(google_search={})],
        temperature=0.3
    )
    
    search_prompt = f"{user_message}\n\nFootprint results: {footprint_response.text}\n\nBudget: £3000. Find actions in Glasgow."
    
    search_response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=search_prompt,
        config=search_config
    )
    
    # Step 3: Format final response with impact summary
    format_instruction = """Format climate recommendations as markdown:

🌍 **Your Carbon Footprint**
- Transport: X.XX tons/year
- Electricity: X.XX tons/year (at Xg/kWh)
- Gas: X.XX tons/year
- Diet: X.XX tons/year
- **Total: X.XX tons/year** (UK average: 10 tons | You're X% below average)

💡 **Top Actions for Glasgow** (ranked by £/ton saved)
1. **[Action]** - £X cost | Saves X.X tons/year | £X/ton
   - Eligibility: [specific criteria]
   - Payback: X years | Bill savings: £X/year
   - Apply: [official link]

🎯 **Total Impact if All Actions Taken**
- CO₂ Reduction: X.X tons/year (X% reduction)
- Bill Savings: £X/year
- Total Cost: £X (within £X budget)
- Contribution to UK Net Zero: Equivalent to [relatable metric]

Use British spelling, emojis, be specific and actionable."""

    format_config = types.GenerateContentConfig(
        system_instruction=format_instruction,
        temperature=0.7
    )
    
    format_prompt = f"Footprint:\n{footprint_response.text}\n\nActions:\n{search_response.text}\n\nFormat this beautifully."
    
    final_response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=format_prompt,
        config=format_config
    )
    
    return final_response
