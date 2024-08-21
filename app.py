import os
import base64
import requests
import streamlit as st

# Access the GPT4V_KEY and GPT4V_ENDPOINT from Streamlit secrets
GPT4V_KEY = st.secrets["GPT4V_KEY"]
GPT4V_ENDPOINT = st.secrets["GPT4V_ENDPOINT"]

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
            "messages": [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": "You are an AI assistant trained to provide detailed descriptions and interpretations of images. Please provide a comprehensive description based on the visual content."
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encoded_image}"
                            }
                        },
                        {
                            "type": "text",
                            "text": f"For the image provided, write brief alternative text of no more than 150 characters. Do not include a summary. Only describe what is in the image: {uploaded_file.name}"
                        }
                    ]
                }
            ],
            "temperature": 0.2,
            "top_p": 0.95,
            "max_tokens": 800
        }

        # Set up headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GPT4V_KEY}",
        }

        # Send the request
        response = requests.post(GPT4V_ENDPOINT, headers=headers, json=payload)

        # Handle the response
        if response.status_code == 200:
            json_response = response.json()
            answer = json_response['choices'][0]['message']['content']
            # Display the answer in the Streamlit app
            st.write(f"Response for {uploaded_file.name}: {answer}")
        else:
            st.error(f"Failed to get a response for {uploaded_file.name}. Status code: {response.status_code}")
