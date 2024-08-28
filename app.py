import os
import base64
import requests
import streamlit as st

# Access the OpenAI API key from Streamlit secrets
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# Set the OpenAI API endpoint
OPENAI_ENDPOINT = "https://api.openai.com/v1/chat/completions"

# Set the page configuration (this sets the page title and icon in the tab)
st.set_page_config(
    page_title="AI-Driven ATLD Generator",
    page_icon="📝",  # Optional: You can use any emoji or a custom icon
)

# Display the page title and description
st.title("AI-Driven Alternative Text and Long Descriptions (ATLD) Generator")

st.markdown("""
**Description**: The purpose of this application is to develop and implement a solution for generating alternative text and long descriptions (ATLD) for images in non-journal content. 
""")

# Streamlit UI for file upload
uploaded_files = st.file_uploader("Upload images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        # Read the image data
        image_data = uploaded_file.read()

        # Encode the image in base64
        encoded_image = base64.b64encode(image_data).decode('ascii')

        # Construct the payload for the request
        payload = {
            "model": "gpt-4o-mini",  # Specify the model that supports vision tasks
            "messages": [
                {
                    "role": "system",
                    "content": "You are an AI assistant trained to provide detailed descriptions and interpretations of images. Please provide a comprehensive description based on the visual content."
                },
                {
                    "role": "user",
                    "content": f"For the image provided, write brief alternative text of no more than 150 characters. Do not include a summary. Only describe what is in the image: {uploaded_file.name}"
                }
            ],
            "temperature": 0.2,
            "top_p": 0.95,
            "max_tokens": 800
        }

        # Set up headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}",
        }

        # Send the request
        response = requests.post(OPENAI_ENDPOINT, headers=headers, json=payload)

        # Handle the response
        if response.status_code == 200:
            json_response = response.json()
            answer = json_response['choices'][0]['message']['content']
            # Display the answer in the Streamlit app
            st.write(f"Response for {uploaded_file.name}: {answer}")
        else:
            st.error(f"Failed to get a response for {uploaded_file.name}. Status code: {response.status_code}")


