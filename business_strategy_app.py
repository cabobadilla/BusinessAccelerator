import streamlit as st
import openai
import json

# Set up the page configuration
st.set_page_config(
    page_title="Business Strategy Agent",
    page_icon="💼",
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

def generate_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional business strategy consultant with expertise in business planning and development."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message['content']
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def main():
    st.title("💼 Business Strategy Agent")
    st.write("Define your business idea and let the agent help you refine and develop a comprehensive strategy.")

    # Initialize session state for storing responses
    if 'refined_idea' not in st.session_state:
        st.session_state.refined_idea = None
    if 'key_elements' not in st.session_state:
        st.session_state.key_elements = None
    if 'marketing_strategies' not in st.session_state:
        st.session_state.marketing_strategies = None

    # Step 1: Define and refine the business idea
    st.header("Step 1: Define Your Business Idea")
    business_idea = st.text_area(
        "Enter your business idea:",
        help="Describe your business idea in detail. What problem does it solve?"
    )
    
    if st.button("Refine Idea"):
        with st.spinner("Analyzing your business idea..."):
            st.session_state.refined_idea = generate_response(
                f"Analyze and refine this business idea. Provide constructive feedback and suggestions for improvement: {business_idea}"
            )
            if st.session_state.refined_idea:
                st.subheader("Refined Business Idea:")
                st.write(st.session_state.refined_idea)

    # Step 2: Specify the product or service
    st.header("Step 2: Specify Product/Service")
    if st.button("Identify Key Elements"):
        if st.session_state.refined_idea:
            with st.spinner("Identifying key elements..."):
                st.session_state.key_elements = generate_response(
                    f"Based on this refined business idea: {st.session_state.refined_idea}\n"
                    "Identify and detail:\n"
                    "1. Key products/services\n"
                    "2. Target market\n"
                    "3. Unique value proposition\n"
                    "4. Required resources\n"
                    "5. Potential challenges"
                )
                if st.session_state.key_elements:
                    st.subheader("Key Elements Analysis:")
                    st.write(st.session_state.key_elements)
        else:
            st.warning("Please complete Step 1 first.")

    # Step 3: Define marketing strategies
    st.header("Step 3: Marketing Strategies")
    if st.button("Define Marketing Strategies"):
        if st.session_state.key_elements:
            with st.spinner("Developing marketing strategies..."):
                st.session_state.marketing_strategies = generate_response(
                    f"Based on these key elements: {st.session_state.key_elements}\n"
                    "Develop a comprehensive marketing strategy including:\n"
                    "1. Marketing channels\n"
                    "2. Customer acquisition strategy\n"
                    "3. Pricing strategy\n"
                    "4. Promotional tactics\n"
                    "5. Brand positioning"
                )
                if st.session_state.marketing_strategies:
                    st.subheader("Marketing Strategy:")
                    st.write(st.session_state.marketing_strategies)
        else:
            st.warning("Please complete Step 2 first.")

    # Step 4: Prepare business strategy and plan
    st.header("Step 4: Business Strategy and Plan")
    if st.button("Prepare Business Strategy"):
        if st.session_state.marketing_strategies:
            with st.spinner("Preparing comprehensive business strategy..."):
                business_strategy = generate_response(
                    f"Based on all previous analysis:\n"
                    f"Refined Idea: {st.session_state.refined_idea}\n"
                    f"Key Elements: {st.session_state.key_elements}\n"
                    f"Marketing Strategies: {st.session_state.marketing_strategies}\n"
                    "Create a comprehensive business strategy including:\n"
                    "1. Executive Summary\n"
                    "2. Financial Projections\n"
                    "3. Implementation Timeline\n"
                    "4. Risk Analysis\n"
                    "5. Success Metrics"
                )
                if business_strategy:
                    st.subheader("Complete Business Strategy:")
                    st.write(business_strategy)
        else:
            st.warning("Please complete Step 3 first.")

    # Add a reset button
    if st.button("Reset All"):
        st.session_state.refined_idea = None
        st.session_state.key_elements = None
        st.session_state.marketing_strategies = None
        st.experimental_rerun()

if __name__ == "__main__":
    main() 