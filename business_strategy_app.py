import streamlit as st
import openai

# Set your OpenAI API key
openai.api_key = 'your-openai-api-key'

def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content']

def main():
    st.title("Business Strategy Agent")
    st.write("Define your business idea and let the agent help you refine and develop a comprehensive strategy.")

    # Step 1: Define and refine the business idea
    st.header("Step 1: Define Your Business Idea")
    business_idea = st.text_area("Enter your business idea:")
    if st.button("Refine Idea"):
        refined_idea = generate_response(f"Refine this business idea: {business_idea}")
        st.write(refined_idea)

    # Step 2: Specify the product or service
    st.header("Step 2: Specify Product/Service")
    if st.button("Identify Key Elements"):
        key_elements = generate_response(f"Identify key elements and processes for this idea: {refined_idea}")
        st.write(key_elements)

    # Step 3: Define marketing strategies
    st.header("Step 3: Marketing Strategies")
    if st.button("Define Marketing Strategies"):
        marketing_strategies = generate_response(f"Define marketing strategies for this product/service: {key_elements}")
        st.write(marketing_strategies)

    # Step 4: Prepare business strategy and plan
    st.header("Step 4: Business Strategy and Plan")
    if st.button("Prepare Business Strategy"):
        business_strategy = generate_response(f"Prepare a business strategy and plan for this idea: {marketing_strategies}")
        st.write(business_strategy)

if __name__ == "__main__":
    main() 