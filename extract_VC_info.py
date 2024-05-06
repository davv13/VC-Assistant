import os
import openai
import json
import streamlit as st

def load_api_key(file_path):
    with open(file_path, 'r') as file:
        return file.readline().strip()

api_key = st.secrets["OPENAI_API_KEY"] if 'OPENAI_API_KEY' in st.secrets else os.getenv('OPENAI_API_KEY')
if not api_key:
    st.error("API key not found. Please set it as an environment variable or in secrets.toml.")
    st.stop()

def extract_vc_details(input_text):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "I have gathered data from the website, I need to extract structured data. Please provide the following details in JSON format: 1. Company Name, 2. Contacts (addresses, phone, email, social media) 3. All Industries that they invest in, 4. Investment rounds that they participate/lead"
            },
            {"role": "user", "content": input_text}
        ]
    )
    data = response.choices[0].message.content
    try:
        structured_data = json.loads(data)
    except json.JSONDecodeError:
        structured_data = {"error": "Failed to decode JSON."}
    return structured_data
