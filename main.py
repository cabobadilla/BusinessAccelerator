import streamlit as st
import openai
import json

# Set up the page configuration
st.set_page_config(
    page_title="Music Playlist Generator",
    page_icon="🎵",
    layout="centered"
)

# Initialize OpenAI API key - Modified for Streamlit Cloud
if 'OPENAI_API_KEY' not in st.session_state:
    st.session_state.OPENAI_API_KEY = st.secrets.get('OPENAI_API_KEY', None)

# API key input for users who want to use their own key
if not st.session_state.OPENAI_API_KEY:
    user_api_key = st.text_input("Enter your OpenAI API key:", type="password")
    if user_api_key:
        st.session_state.OPENAI_API_KEY = user_api_key

# Check if API key is available
if not st.session_state.OPENAI_API_KEY:
    st.warning("Please add your OpenAI API key to continue.")
    st.stop()

# Set the API key for OpenAI
openai.api_key = st.session_state.OPENAI_API_KEY

# ... rest of your code remains the same ... 