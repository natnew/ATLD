import streamlit as st
import requests
import base64

# Streamlit UI
st.title("AI-Generated Alternative Text and Long Descriptions")

# API key input
gpt4v_key = st.text_input("Enter the GPT-4V API key:", type="password")
gpt4v_endpoint = st.text_input("Enter the GPT-4V endpoint:")

# File uploader
uploaded_files = st.file_uploader("Upload image files", accept_multiple_files=True, type=["jpg", "jpeg", "png"])

# Process the images and generate descriptions
if st.button("Generate Descriptions"):
    if not gpt4v_key or not gpt4v_endpoint:
        st.error("Please provide the API key and endpoint.")
    elif uploaded_files:
        for uploaded_file in uploaded_files:
            # Read image data
            image_data = uploaded_file.read()
            encoded_image = base64.b64encode(image_data).decode('ascii')

            # Create payload
            payload = {
                "messages": [
                    {
                        "role": "system",
                        "content": [{
                            "type": "text",
                            "text": "You are an AI assistant trained to provide detailed descriptions and interpretations of images. Please provide a comprehensive description based on the visual content."
                        }]
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
                                "text": f"For the image provided, write brief alternative text of no more than 150 characters. Do not include a summary. Only describe what is in the image."
                            }
                        ]
                    }
                ],
                "temperature": 0.2,
                "top_p": 0.95,
                "max_tokens": 800
            }

            # Headers for the request
            headers = {
                "Content-Type": "application/json",
                "api-key": gpt4v_key,
            }

            # Send request to the endpoint
            response = requests.post(gpt4v_endpoint, headers=headers, json=payload)
            if response.status_code == 200:
                json_response = response.json()
                answer = json_response['choices'][0]['message']['content']
                st.image(uploaded_file)
                st.write(f"**Description for {uploaded_file.name}:** {answer}")
            else:
                st.error(f"Failed to generate description for {uploaded_file.name}. Status code: {response.status_code}")
    else:
        st.error("Please upload at least one image file.")

# Optionally, you can add a download button to save the generated descriptions.

