import streamlit as st
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import os
from dotenv import load_dotenv
import asyncio
import sys

# Add src to path for agent discovery
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from climate_concierge.agents.climate_coordinator.agent import root_agent

load_dotenv()

st.set_page_config(page_title="UK Climate Action Concierge", page_icon="🌍")

st.title("🌍 UK Climate Action Concierge")
st.caption("Powered by Google ADK • Multi-agent climate recommendations")

# API Key
api_key = st.sidebar.text_input("Google AI API Key", value=os.getenv("GOOGLE_API_KEY", ""), type="password")

if not api_key:
    st.info("👈 Enter your Google AI API key")
    st.stop()

os.environ["GOOGLE_API_KEY"] = api_key

# Initialize Runner and Session
if "runner" not in st.session_state:
    session_service = InMemorySessionService()
    st.session_state.runner = Runner(
        app_name="climate_concierge",
        agent=root_agent,
        session_service=session_service
    )
    st.session_state.user_id = "user123"
    
    # Create session
    async def create_session():
        return await session_service.create_session(
            app_name="climate_concierge",
            user_id="user123"
        )
    
    session = asyncio.run(create_session())
    st.session_state.session_id = session.id

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("E.g., I drive 5000 miles/year, eat meat daily, use 3000 kWh electricity, 12000 kWh gas, live in Glasgow, budget £3000"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("🤖 Multi-agent: FootprintCalculator → ActionRecommender → ResponseFormatter"):
            try:
                message = types.Content(role='user', parts=[types.Part(text=prompt)])
                
                async def run_agent():
                    response_text = ""
                    last_response = ""
                    async for event in st.session_state.runner.run_async(
                        user_id=st.session_state.user_id,
                        session_id=st.session_state.session_id,
                        new_message=message
                    ):
                        if event.content and event.content.parts:
                            for part in event.content.parts:
                                if part.text:
                                    last_response = part.text
                    return last_response
                
                result = asyncio.run(run_agent())
                
                if result:
                    st.markdown(result)
                    st.session_state.messages.append({"role": "assistant", "content": result})
                else:
                    st.error("No response")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Sidebar
with st.sidebar:
    st.markdown("---")
    st.subheader("🤖 ADK Multi-Agent")
    st.markdown("""
    **Coordinator** orchestrates:
    1. **FootprintCalculator** - Live UK grid + code
    2. **ActionRecommender** - Google Search
    3. **ResponseFormatter** - Markdown
    
    Proper ADK folder structure!
    """)
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
