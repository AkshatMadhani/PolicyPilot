import streamlit as st
from phi.agent import Agent
from phi.tools.exa import ExaTools
from phi.model.groq import Groq
from dotenv import load_dotenv
import os
from PyPDF2 import PdfReader

load_dotenv()
EXA_API_KEY=st.secrets("EXA_API_KEY"),
GROQ_API_KEY=st.secrets("GROQ_API_KEY")

claim_agent = Agent(
    name="Claim Assistance Agent",
    model=Groq(id='llama-3.1-8b-instant'),
    tools=[ExaTools()],
    markdown=True,
    description="You are an expert claim processing assistant. Your role is to guide users in claiming their policies efficiently, minimizing stress and ensuring a seamless process.",
    instructions = [
    "Use Exa to extract relevant claim information from trusted insurance platforms and documents.",
    "Collect details on required documents, timelines, and claim-specific requirements for the user’s policy.",
    "Ensure all provided information is accurate, easy to follow, and tailored to the user’s claim type and reason.",
    "Guide the user step-by-step through the claim process, including mandatory and optional documents, necessary actions, and timeframes.",
    "Offer tips and advice to help avoid common claim rejections and ensure faster approval.",
    "Do not provide external links or specific provider names in the response."
]
)


st.title("Policy Claim Assistance")

claim_type = st.selectbox(
    "Select the Nature of Your Claim",
    ["Accidental Damage", "Theft or Loss", "Natural Disaster", "Medical Emergency", "Other"]
)
policy_id = st.text_input("Enter your Policy ID")
claim_reason = st.text_area("Describe the reason for your claim")

uploaded_files = st.file_uploader("Upload relevant documents or photos related to the claim", type=["jpg", "jpeg", "png", "pdf"], accept_multiple_files=True)


def extract_text_from_pdf(uploaded_file):
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


if st.button("Get Claim Assistance"):
    user_query = f"""
    I need assistance with my insurance claim (Policy ID: {policy_id}) for {claim_reason} (Claim Type: {claim_type}).
    Please guide me on the fastest way to:
    - Complete the claim submission.
    - Provide a list of required and optional documents.
    - Outline expected timelines for approval.
    - Suggest tips to avoid delays or rejection.
    - Provide any contact points or resources if I need additional help.
"""



    with st.spinner("Processing your claim..."):
        response = claim_agent.run(user_query)

        
        st.write(response.content)

        
        if uploaded_files:
            st.write("Uploaded Files:")
            for uploaded_file in uploaded_files:
                st.write(uploaded_file.name)
