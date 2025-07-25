import streamlit as st
from PIL import Image

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
    image = Image.open(uploaded_file)
    st.image(image, caption="📸 Uploaded Label", use_column_width=True)