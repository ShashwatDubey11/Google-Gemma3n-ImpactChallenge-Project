import streamlit as st
from PIL import Image
import requests  # For sending the image to an API (if needed)

st.set_page_config(page_title="Label Decoder", layout="centered")
st.title("📷 Label Decoder - Upload a Product Label")

# Create tabs for different input methods
tab1, tab2 = st.tabs(["📷 Camera", "📁 Upload File"])

uploaded_file = None

with tab1:
    uploaded_file = st.camera_input("Take a photo of the label")

with tab2:
    if not uploaded_file:  # Only show file uploader if no camera input
        uploaded_file = st.file_uploader("Upload an image file", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="📸 Uploaded Label", use_column_width=True)

    # Add the "Analyze This" button
    if st.button("Analyze This"):
        # Save the uploaded image locally
        image_path = f"uploads/{uploaded_file.name}"
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"Image saved at: {image_path}")

        # Call your API or Python script for analysis
        # Example: Sending the image to an API
        with st.spinner("Analyzing the image..."):
            try:
                # Replace with your API endpoint
                api_url = "http://127.0.0.1:5000/analyze"
                files = {"file": open(image_path, "rb")}
                response = requests.post(api_url, files=files)
                
                if response.status_code == 200:
                    st.markdown("### Analysis Results")
                    st.write(response.json())  # Display the API response
                else:
                    st.error(f"API Error: {response.status_code}")
            except Exception as e:
                st.error(f"Error: {e}")