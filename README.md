# 🌍 UK Climate Action Concierge

AI-powered climate action recommendations using Google ADK. Calculates your carbon footprint and finds UK-specific grants, tariffs, and actions ranked by cost-effectiveness.

## Features
- ✅ Live UK grid carbon intensity
- ✅ Precise footprint calculation (transport, diet, energy)
- ✅ Real-time search for UK grants (ECO4, BUS, etc.)
- ✅ Cost-benefit ranking
- ✅ Multi-turn conversations with memory

## Setup

1. **Get API Key**: Free at [aistudio.google.com](https://aistudio.google.com)

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Run the app**:
   ```bash
   uv run streamlit run app.py
   ```

4. **Enter API key** in the sidebar and start chatting!

## Example Query

```
I drive 5000 miles/year, eat meat daily, use 3000 kWh electricity and 12000 kWh gas, 
live in Glasgow (G1 postcode), and have £3000 budget for climate actions.
```

## Agentic Architecture

### Overview
This project implements a **multi-agent workflow** using Google Gemini 2.5 Flash lite, where specialized agents collaborate to deliver personalized UK climate recommendations. Each agent has a specific role and uses dedicated tools to accomplish its task.

### Agent Flow
```
User Query → FootprintCalculatorAgent → ActionRecommenderAgent → ResponseFormatterAgent → Final Output
```

### Agents

#### 1. FootprintCalculatorAgent
**Purpose**: Calculate precise carbon footprint from user's lifestyle data

**Tools**:
- **Code Execution** (Gemini built-in): Runs Python code for precise calculations
- **UK Carbon Intensity API** (custom): Fetches live grid carbon intensity by postcode

**Process**:
1. Extracts transport (miles/year), energy (kWh), diet, and location from user input
2. Fetches live grid intensity from `api.carbon-intensity.org.uk` for user's postcode
3. Calculates emissions using 2025 UK factors:
   - Transport: 0.207 kgCO₂/mile (petrol/diesel avg)
   - Electricity: Live grid intensity (e.g., 141 gCO₂/kWh for Glasgow)
   - Gas: 0.183 kgCO₂/kWh
   - Diet: 1.2 kgCO₂/day for meat-heavy
4. Returns breakdown: `{transport: X, electricity: Y, gas: Z, diet: W, total: T}`

**Output Example**:
```
Transport: 1.03 tons
Electricity: 0.42 tons (at 141g/kWh)
Gas: 2.20 tons
Diet: 0.44 tons
Total: 4.09 tons/year (UK avg: 10 tons)
```

---

#### 2. ActionRecommenderAgent
**Purpose**: Find UK-specific climate actions, grants, and tariffs ranked by cost-effectiveness

**Tools**:
- **Google Search** (Gemini built-in): Searches for latest grants, schemes, and tariffs
- **Code Execution** (Gemini built-in): Calculates £/ton saved and ranks actions

**Process**:
1. Searches for location-specific actions:
   - "ECO4 grant [city] 2025 eligibility"
   - "Home Energy Scotland ASHP grant"
   - "Octopus Agile tariff savings"
   - "Loft insulation cost [city]"
   - "Cycle to Work scheme UK"
2. Extracts from search results:
   - Cost (after grants)
   - Tons CO₂ saved/year
   - Eligibility criteria (income, EPC rating, benefits)
   - Official apply links
3. Calculates cost-effectiveness: `£/ton = cost / (tons_saved × 10 years)`
4. Filters actions ≤ user budget
5. Ranks: Free actions first, then lowest £/ton

**Output Example**:
```
1. ECO4 Insulation - £0 | 1.7 tons/year | £0/ton
   Eligibility: Income <£31k, EPC D-G, Glasgow
   Apply: gov.uk/eco4

2. ASHP Grant - £0 net | 1.7 tons/year | £0/ton
   Eligibility: Home Energy Scotland, up to £9k grant
   Apply: homeenergyscotland.org
```

---

#### 3. ResponseFormatterAgent
**Purpose**: Format results into beautiful, actionable markdown

**Tools**: None (pure LLM reasoning)

**Process**:
1. Takes footprint data + action recommendations
2. Formats into structured markdown with:
   - 🌍 Carbon footprint breakdown
   - 💡 Top 5 ranked actions with eligibility/payback
   - 🎯 Total impact summary (CO₂ reduction, bill savings, % improvement)
3. Uses British spelling, emojis, and concise language
4. Adds relatable metrics (e.g., "Equivalent to planting 200 trees")

**Output Example**:
```markdown
🎯 Total Impact if All Actions Taken
- CO₂ Reduction: 4.42 tons/year (52% reduction)
- Bill Savings: £800/year
- Total Cost: £900 (within £3000 budget)
```

---

### Tools & APIs

| Tool | Type | Source | Cost | Purpose |
|------|------|--------|------|----------|
| **Code Execution** | Gemini built-in | Google | Free | Precise calculations, data processing |
| **Google Search** | Gemini built-in | Google | Free | Find latest grants, tariffs, schemes |
| **UK Carbon Intensity API** | Custom REST API | carbon-intensity.org.uk | Free | Live grid carbon intensity by postcode |

### Why This Architecture?

1. **Separation of Concerns**: Each agent has a single, well-defined responsibility
2. **Tool Specialization**: Agents use only the tools they need (e.g., Calculator doesn't search)
3. **Accuracy**: Code execution ensures precise math; live API provides real-time data
4. **Scalability**: Easy to add new agents (e.g., TransportAgent for EV recommendations)
5. **Transparency**: Clear flow makes debugging and improvements straightforward

### Technical Stack
- **LLM**: Google Gemini 2.5 Flash lite (fast, supports tools, 1M token context)
- **Framework**: Streamlit (interactive web UI)
- **Language**: Python 3.13
- **Package Manager**: uv (fast, reliable dependency management)
