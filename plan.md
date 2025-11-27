* IMPORTANT NOTE: You can see the complete plan below but before implementation, first use uv init to initialise virtual env and to install dependencies inside venv. Also, please access latest ADK documentation for correct code and for debugging. 

### Google's ADK(Agent Development Kit) High-Level Agentic Architecture (Production-Ready for Our Project)

```
CoordinatorAgent (Gemini 2.5 Flash-Lite)
│
├── 1. FootprintCalculatorAgent
│   ├── Tools:
│   │   ├─ CodeExecutor                  → precise math (miles × 0.25 kgCO₂, etc.)
│   │   └─ UKCarbonIntensityTool         → live gCO₂/kWh from carbon-intensity.org.uk
│   └── Output: {"transport_tons": 3.1, "diet_tons": 2.4, "energy_tons": 2.8, "total_tons": 8.3}
│
├── 2. ActionRecommenderAgent
│   ├── Tools:
│   │   ├─ GoogleSearchTool (built-in)   → "ECO4 grants Glasgow 2025" / "Octopus Agile tariff" / "Boiler Upgrade Scheme Scotland"
│   │   ├─ UrlContextTool                → scrape & summarise gov.uk / energy supplier pages
│   │   └─ CodeExecutor                  → rank results by £ per ton saved, filter ≤ user budget
│   └── Output: List of 3–5 actions with exact £ cost, tons saved, and direct apply link
│
├── 3. ResponseFormatterAgent
│   └── Tools: none (pure LLM)
│       → Turns structured JSON into beautiful UK-friendly markdown + emojis
│
└── Memory (ADK SessionState)
    → Stores user facts across turns (so follow-up questions work)
```

### Tool Definitions (All Free)

| Tool                     | Type           | Source                        | Key Required? | Usage in Project                     |
|--------------------------|----------------|-------------------------------|---------------|--------------------------------------|
| GoogleSearchTool         | ADK built-in   | Google via Gemini             | No            | Find latest UK grants/tariffs        |
| UrlContextTool           | ADK built-in   | Direct page fetch             | No            | Read gov.uk eligibility pages        |
| CodeExecutor             | ADK built-in   | Sandboxed Python              | No            | All calculations & ranking           |
| UKCarbonIntensityTool    | Custom         | https://api.carbon-intensity.org.uk | No            | Live grid intensity (national + regions) |

### Backend Flow (One Query)

1. User → CoordinatorAgent  
2. Coordinator → FootprintCalculatorAgent → returns JSON footprint  
3. Coordinator → ActionRecommenderAgent (passes footprint + budget + city) → returns ranked actions  
4. Coordinator → ResponseFormatterAgent → final markdown  
5. Streamlit → displays result

## Strict Requirements
### Features to Include in Your Agent Submission
In your submission, you must demonstrate what you’ve learned in this course by applying at least three (3) of the key concepts listed below:

* ✅ Multi-agent system, including any combination of:
    * ✅ Agent powered by an LLM
    * ❌ Parallel agents
    * ✅ Sequential agents
    * ❌ Loop agents
* ✅ Tools, including:
    * ❌ MCP
    * ✅ custom tools
    * ✅ built-in tools, such as Google Search or Code Execution
    * ❌ OpenAPI tools
    * ❌ Long-running operations (pause/resume agents)
* ✅ Sessions & Memory
    * ✅ Sessions & state management (e.g. InMemorySessionService)
    * ❌ Long term memory (e.g. Memory Bank)
* ❌ Context engineering (e.g. context compaction)
* ❌ Observability: Logging, Tracing, Metrics
* ❌ Agent evaluation
* ❌ A2A Protocol
* ❌ Agent deployment