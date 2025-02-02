import streamlit as st
from phi.agent import Agent
from phi.tools.exa import ExaTools
from phi.model.groq import Groq
from dotenv import load_dotenv

load_dotenv()
EXA_API_KEY=st.secrets["EXA_API_KEY"],
GROQ_API_KEY=st.secrets["GROQ_API_KEY"],                      
policy_recommender_agent = Agent(
    name="Policy Recommender",
    model=Groq(id='llama-3.1-8b-instant'),
    tools=[ExaTools()],
    markdown=True,
    description="You are an expert insurance policy advisor. Your role is to assist users in finding the best policies tailored to their preferences and needs.",
    instructions=[
        "Use Exa to search and extract relevant data from trusted and reputable insurance platforms.",
        "Gather comprehensive information on various insurance policies, including health, life, and investment-based options.",
        "Ensure the data is accurate and tailored to the user's preferences, such as age, income  and health condition", 
        "Provide clear and concise recommendations that include: policy name, coverage details, benefits, estimated premiums, maturity or return options, and any special features (e.g., tax benefits).",
        "If a particular policy or provider is unavailable, provide alternative suggestions from other reliable sources.",
        "Avoid including direct links to external websites or specific provider names  in the response.",
        "Ensure that the recommendations focus on user satisfaction and provide the best possible outcomes under any circumstance.",
        
    ]
)

st.title("Policy Advisor Agent")


name = st.text_input("Enter your name")
age = st.number_input("Enter your age", min_value=18, max_value=100, value=30)
income = st.number_input("Enter your monthly income (INR)", min_value=5000, max_value=1000000, value=50000)
disease = st.text_input("Any severe disease (e.g., diabetes)")

if st.button("Generate Policy Recommendation"):
    user_query = f"""
    My name is {name}. I am {age} years old, with a monthly income of {income} INR. 
    I am looking for the best insurance policy tailored to my needs and income. 
    I have {disease or 'no specific health conditions'} and want a policy that offers good returns and  coverage in all circumstances. 
    Please recommend policies with their benefits, coverage details, approximate premiums, and special features, ensuring the suggestions focus on my satisfaction.
    """
    
    with st.spinner("Processing..."):
        response = policy_recommender_agent.run(user_query)
    
    st.write(response.content)
