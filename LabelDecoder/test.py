

import streamlit as st
import os
from dotenv import load_dotenv

# Force reload environment variables
load_dotenv(override=True)

st.title("🔧 Debug: Environment Variables")

# Check if API key is loaded
api_key = os.getenv('GEMINI_API_KEY')

st.write("**Environment Variables Check:**")
st.write(f"- API Key loaded: {'✅ Yes' if api_key else '❌ No'}")

if api_key:
    st.write(f"- API Key length: {len(api_key)}")
    st.write(f"- API Key preview: {api_key[:10]}...{api_key[-4:]}")
    
    # Test the API key in Streamlit context
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        if st.button("Test API Key"):
            with st.spinner("Testing API key..."):
                response = model.generate_content("Say hello in one word")
                st.success(f"✅ API Key works! Response: {response.text}")
    except Exception as e:
        st.error(f"❌ API Key test failed: {e}")
else:
    st.error("❌ API Key not found")

# Show all environment variables (for debugging)
with st.expander("All Environment Variables"):
    for key, value in os.environ.items():
        if 'GEMINI' in key or 'API' in key:
            st.write(f"**{key}**: {value[:10]}..." if value else f"**{key}**: None")