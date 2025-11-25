import streamlit as st
from google import genai
from agents import get_climate_recommendations
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="UK Climate Action Concierge", page_icon="🌍")

st.title("🌍 UK Climate Action Concierge")
st.caption("Powered by Google Gemini • Free UK-specific climate recommendations")

# API Key input
api_key = st.sidebar.text_input("Google AI API Key", value=os.getenv("GOOGLE_API_KEY", ""), type="password", help="Get free key at aistudio.google.com")

if not api_key:
    st.info("👈 Enter your Google AI API key in the sidebar to start")
    st.stop()

# Initialize client
client = genai.Client(api_key=api_key)

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("E.g., I drive 5000 miles/year, eat meat daily, use 3000 kWh electricity, live in Glasgow, budget £3000"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Analyzing your footprint and finding actions..."):
            try:
                response = get_climate_recommendations(client, prompt)
                result = response.text
                st.markdown(result)
                st.session_state.messages.append({"role": "assistant", "content": result})
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.error(f"Full error: {repr(e)}")

# Sidebar info
with st.sidebar:
    st.markdown("---")
    st.subheader("How it works")
    st.markdown("""
    1. **Calculate** your carbon footprint
    2. **Find** UK grants & tariffs
    3. **Rank** by cost-effectiveness
    
    All data is live from UK APIs.
    """)
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
