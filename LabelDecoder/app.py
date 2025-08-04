"""
Label Decoder - AI-Powered Product Label Analyzer
A Streamlit application that uses Google Gemini AI to analyze product labels
and provide detailed information about ingredients, health impacts, and more.
"""

import streamlit as st
from PIL import Image
import os
import json
from datetime import datetime

# Import our custom modules
from database.db_manager import db_manager
from utils.gemini_analyzer import create_gemini_analyzer
from utils.image_handler import image_handler
from config.settings import config

# Configure Streamlit page
st.set_page_config(
    page_title=config.PAGE_TITLE,
    page_icon=config.PAGE_ICON,
    layout="centered",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Initialize session state variables."""
    if 'analysis_history' not in st.session_state:
        st.session_state.analysis_history = []
    if 'current_image_id' not in st.session_state:
        st.session_state.current_image_id = None

def render_sidebar():
    """Render the sidebar with configuration and statistics."""
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key input
        api_key = st.text_input(
            "Google Gemini API Key",
            type="password",
            help="Enter your Google Gemini API key. Get one from: https://aistudio.google.com/app/apikey"
        )
        
        if api_key:
            st.session_state.gemini_api_key = api_key
            st.success("✅ API Key configured!")
        else:
            st.warning("⚠️ Please enter your Gemini API key to use the analyzer.")
        
        st.divider()
        
        # Statistics
        st.header("📊 Statistics")
        stats = db_manager.get_upload_statistics()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Uploads", stats['total_uploads'])
        with col2:
            st.metric("Completed", stats['completed_analyses'])
        
        st.metric("Pending", stats['pending_analyses'])
        
        st.divider()
        
        # Recent uploads
        st.header("📝 Recent Uploads")
        recent = db_manager.get_recent_uploads(limit=5)
        
        if recent:
            for upload in recent:
                with st.expander(f"📷 {upload['original_filename'][:20]}..."):
                    st.write(f"**Status:** {upload['analysis_status']}")
                    st.write(f"**Date:** {upload['upload_timestamp']}")
                    st.write(f"**Size:** {upload['file_size']} bytes")
        else:
            st.info("No uploads yet")

def render_main_interface():
    """Render the main application interface."""
    st.title("📷 Label Decoder - AI Product Label Analyzer")
    st.markdown("""
    Upload a photo of any product label and get detailed analysis including:
    - Ingredient breakdown
    - Health impact assessment  
    - Allergen warnings
    - Nutritional information
    - Safety recommendations
    """)
    
    # Create tabs for different input methods
    tab1, tab2 = st.tabs(["📷 Take Photo", "📁 Upload File"])
    
    uploaded_file = None
    
    with tab1:
        st.markdown("### 📸 Take a Photo")
        uploaded_file = st.camera_input("Point your camera at the product label")
    
    with tab2:
        st.markdown("### 📂 Upload Image File")
        if not uploaded_file:  # Only show file uploader if no camera input
            uploaded_file = st.file_uploader(
                "Choose an image file",
                type=["png", "jpg", "jpeg", "gif", "bmp", "webp"],
                help="Supported formats: PNG, JPG, JPEG, GIF, BMP, WEBP"
            )
    
    return uploaded_file

def process_uploaded_image(uploaded_file):
    """Process the uploaded image and display it."""
    if uploaded_file is None:
        return None
    
    # Validate the image
    is_valid, message = image_handler.validate_image(uploaded_file)
    if not is_valid:
        st.error(f"❌ {message}")
        return None
    
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="📸 Uploaded Label", use_column_width=True)
    
    # Show image info
    with st.expander("📋 Image Information"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"**Filename:** {uploaded_file.name}")
        with col2:
            st.write(f"**Size:** {uploaded_file.size} bytes")
        with col3:
            st.write(f"**Type:** {getattr(uploaded_file, 'type', 'Unknown')}")
    
    return uploaded_file

def analyze_image(uploaded_file):
    """Analyze the uploaded image using Gemini AI."""
    if 'gemini_api_key' not in st.session_state:
        st.error("❌ Please configure your Gemini API key in the sidebar first.")
        return
    
    # Save the image
    success, message, file_info = image_handler.save_uploaded_image(uploaded_file)
    
    if not success:
        st.error(f"❌ Failed to save image: {message}")
        return
    
    # Save to database
    image_id = db_manager.save_uploaded_image(
        file_info['filename'],
        file_info['original_filename'],
        file_info['file_path'],
        file_info['file_size']
    )
    
    st.session_state.current_image_id = image_id
    st.success(f"✅ Image saved successfully!")
    
    # Analyze with Gemini
    with st.spinner("🔍 Analyzing the image with AI... This may take a few moments."):
        try:
            # Create Gemini analyzer
            analyzer = create_gemini_analyzer(st.session_state.gemini_api_key)
            
            if not analyzer.is_configured():
                st.error("❌ Failed to configure Gemini API. Please check your API key.")
                return
            
            # Perform analysis
            result = analyzer.analyze_label_image(file_info['file_path'])
            
            if result['success']:
                # Save analysis to database
                analysis_data = result['data']
                db_manager.save_analysis_result(
                    image_id,
                    analysis_data['raw_text'],
                    json.dumps(analysis_data['processed_data']),
                    analysis_data['model_used']
                )
                
                # Display results
                display_analysis_results(analysis_data)
                
                # Add to session history
                st.session_state.analysis_history.append({
                    'timestamp': datetime.now(),
                    'filename': file_info['original_filename'],
                    'result': analysis_data
                })
                
            else:
                st.error(f"❌ Analysis failed: {result['error']}")
                
        except Exception as e:
            st.error(f"❌ Error during analysis: {str(e)}")

def display_analysis_results(analysis_data):
    """Display the analysis results in a structured format."""
    st.markdown("## 🔍 Analysis Results")
    
    # Quick summary
    processed_data = analysis_data.get('processed_data', {})
    
    # Health rating display
    health_rating = processed_data.get('health_rating')
    if health_rating:
        # Create a visual health meter
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            # Color-coded health rating
            if health_rating >= 8:
                color = "🟢"
                status = "Excellent"
            elif health_rating >= 6:
                color = "🟡"
                status = "Good"
            elif health_rating >= 4:
                color = "🟠"
                status = "Fair"
            else:
                color = "🔴"
                status = "Poor"
            
            st.markdown(f"""
            <div style="text-align: center; padding: 20px; border-radius: 10px; background-color: #f0f2f6;">
                <h3>Health Rating</h3>
                <h1>{color} {health_rating}/10</h1>
                <h4>{status}</h4>
            </div>
            """, unsafe_allow_html=True)
    
    # Key insights
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🧪 Key Ingredients")
        ingredients = processed_data.get('key_ingredients', [])
        if ingredients:
            for ingredient in ingredients[:5]:
                if ingredient.strip():
                    st.write(f"• {ingredient}")
        else:
            st.write("No ingredients extracted")
    
    with col2:
        st.subheader("⚠️ Warnings")
        warnings = processed_data.get('warnings', [])
        if warnings:
            for warning in warnings:
                if warning.strip():
                    st.warning(f"⚠️ {warning}")
        else:
            st.success("No specific warnings found")
    
    # Full analysis text
    st.subheader("📋 Detailed Analysis")
    with st.expander("View Full Analysis", expanded=True):
        raw_text = analysis_data.get('raw_text', 'No analysis text available')
        st.markdown(raw_text)
    
    # Analysis metadata
    with st.expander("🔧 Analysis Details"):
        st.write(f"**Model Used:** {analysis_data.get('model_used', 'Unknown')}")
        st.write(f"**Image Path:** {analysis_data.get('image_path', 'Unknown')}")
        st.write(f"**Analysis Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    """Main application function."""
    # Initialize session state
    initialize_session_state()
    
    # Render sidebar
    render_sidebar()
    
    # Render main interface
    uploaded_file = render_main_interface()
    
    # Process uploaded image
    if uploaded_file:
        processed_file = process_uploaded_image(uploaded_file)
        
        if processed_file:
            # Add analyze button
            if st.button("🔍 Analyze This Label", type="primary", use_container_width=True):
                analyze_image(processed_file)
    
    # Show recent analysis if available
    if st.session_state.analysis_history:
        st.divider()
        st.subheader("📈 Recent Analyses")
        
        # Show last analysis
        last_analysis = st.session_state.analysis_history[-1]
        with st.expander(f"Latest: {last_analysis['filename']}", expanded=False):
            display_analysis_results(last_analysis['result'])

if __name__ == "__main__":
    main()