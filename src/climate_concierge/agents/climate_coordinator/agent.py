from google.adk.agents import SequentialAgent
from ..footprint_calculator.agent import root_agent as footprint_agent
from ..action_recommender.agent import root_agent as action_agent
from ..response_formatter.agent import root_agent as formatter_agent

root_agent = SequentialAgent(
    name="climate_concierge",
    description="Sequential workflow: calculate footprint → find actions → format response",
    sub_agents=[footprint_agent, action_agent, formatter_agent]
)
