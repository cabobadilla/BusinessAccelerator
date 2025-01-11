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
                f"""Analyze this business idea and provide a concise but complete definition in 3-4 sentences maximum. Include:
                1. Core value proposition
                2. Target market
                3. Revenue model
                4. Key differentiators
                
                Business idea: {business_idea}"""
            )
            if st.session_state.refined_idea:
                st.subheader("Refined Business Idea:")
                st.write(st.session_state.refined_idea)

    # Step 2: Define Customer and Product Details
    st.header("Step 2: Customer & Product Analysis")
    if st.button("Analyze Core Elements"):
        if st.session_state.refined_idea:
            with st.spinner("Analyzing critical business elements..."):
                st.session_state.key_elements = generate_response(
                    f"Based on this refined business idea: {st.session_state.refined_idea}\n"
                    "Provide a detailed analysis focusing on the most critical initial elements:\n"
                    "1. Target Customer Profile:\n"
                    "   - Detailed demographic characteristics (e.g., 'Urban professionals aged 25-45, income >$75k/year')\n"
                    "   - Key pain points and needs (e.g., 'Lack of time for meal prep, desire for healthy options')\n" 
                    "   - Customer behavior patterns (e.g., 'Orders food delivery 3-4x/week, checks phone during commute')\n"
                    "   - Willingness and ability to pay (e.g., 'Spends $15-25 per meal, values convenience over cost')\n\n"
                    "2. Product/Service Specification:\n"
                    "   - Core features and functionalities (e.g., 'Mobile app with 1-click ordering, dietary preference filters')\n"
                    "   - Unique selling propositions (e.g., 'Only service offering same-day organic meal prep delivery')\n"
                    "   - Minimum viable product (MVP) definition (e.g., 'Basic ordering system + 3 meal options + delivery')\n"
                    "   - Product-market fit analysis (e.g., 'High alignment with target users based on survey of 100 customers')\n\n"
                    "3. Initial Go-to-Market Strategy:\n"
                    "   - Primary customer acquisition channels (e.g., 'Instagram ads, local fitness partnerships, referral program')\n"
                    "   - Key messaging and positioning (e.g., 'Healthy eating made effortless for busy professionals')\n"
                    "   - Initial pricing strategy (e.g., 'Freemium model: Basic free, Premium at $19.99/month')"
                )
                if st.session_state.key_elements:
                    st.subheader("Core Business Elements:")
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
                    "Develop a detailed marketing strategy focused on the specific product/service and target customers identified. Include:\n"
                    "1. Product Marketing Strategy:\n"
                    "   - Key product features and benefits to highlight (e.g., 'AI-powered automation saves 20 hours per month')\n"
                    "   - Product positioning and messaging (e.g., 'The most intuitive accounting software for small businesses')\n"
                    "   - Value proposition and competitive advantages (e.g., '50% cost reduction vs traditional solutions')\n\n"
                    "2. Customer Targeting Plan:\n" 
                    "   - Detailed customer persona profiles (e.g., 'Sarah, 45, small business owner, $2M annual revenue')\n"
                    "   - Customer journey mapping (e.g., 'Awareness through LinkedIn → Website visit → Free trial → Purchase')\n"
                    "   - Touchpoint optimization strategy (e.g., 'Personalized email sequences based on user behavior')\n\n"
                    "3. Channel Strategy:\n"
                    "   - Specific marketing channels to use (e.g., 'LinkedIn Ads, Google Search, Industry podcasts')\n"
                    "   - Content and messaging for each channel (e.g., 'LinkedIn: Educational posts about automation ROI')\n"
                    "   - Channel performance metrics and optimization approach (e.g., 'CAC < $200, 3x ROAS target')"
                )
                if st.session_state.marketing_strategies:
                    st.subheader("Marketing Strategy:")
                    st.write(st.session_state.marketing_strategies)
        else:
            st.warning("Please complete Step 2 first.")

    # Step 4: Prepare business strategy and plan
    st.header("Step 4: Final Business Strategy")
    if st.button("Generate Complete Business Strategy"):
        if st.session_state.marketing_strategies:
            with st.spinner("Consolidating business strategy..."):
                business_strategy = generate_response(
                    f"Based on previous analysis:\n"
                    f"Refined Idea: {st.session_state.refined_idea}\n"
                    f"Key Elements: {st.session_state.key_elements}\n"
                    f"Marketing Strategies: {st.session_state.marketing_strategies}\n"
                    "Create a clear and actionable business strategy including:\n"
                    "1. Business Overview\n"
                    "   - Core value proposition (e.g., 'We help small businesses reduce accounting costs by 50% through AI automation')\n"
                    "   - Detailed target market analysis with specific examples of ideal customers\n"
                    "   - Revenue model breakdown with pricing tiers and revenue streams\n"
                    "   - Competitive landscape analysis with direct competitor examples\n\n"
                    "2. Go-to-Market Strategy\n"
                    "   - Detailed customer acquisition funnel (e.g., LinkedIn ads → Landing page → Free trial → Paid conversion)\n"
                    "   - Channel-specific marketing tactics with content examples\n"
                    "   - Pricing strategy with specific package examples\n"
                    "   - Partnership and distribution strategy\n\n"
                    "3. Key Activities and Timeline\n"
                    "   - First 90 days roadmap with specific milestones\n"
                    "   - Required resources and detailed budget allocation\n"
                    "   - Strategic partnerships to pursue with examples\n"
                    "   - Risk assessment and mitigation strategies with real-world scenarios\n\n"
                    "Please provide concrete examples and specific details for each section to make the strategy more actionable."
                )
                if business_strategy:
                    st.subheader("Your Complete Business Strategy:")
                    st.write(business_strategy)
                    
                    st.success("🎉 Congratulations! You now have a complete business strategy. Focus on executing these key elements to bring your idea to life.")
        else:
            st.warning("Please complete the previous steps first.")

    # Add a reset button
    if st.button("Reset All"):
        st.session_state.refined_idea = None
        st.session_state.key_elements = None
        st.session_state.marketing_strategies = None
        st.experimental_rerun()

if __name__ == "__main__":
    main() 