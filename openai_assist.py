import os
import openai
import json

def load_api_key(file_path):
    with open(file_path, 'r') as file:
        return file.readline().strip()

api_key_path = 'openai_api_key.txt'
openai.api_key = load_api_key(api_key_path)

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


# vc_details = extract_vc_details('www.accel.com.md')

vc_details = extract_vc_details('www.a16z.com.md')

print(json.dumps(vc_details, indent=4))
