"""
Configuration settings for the Label Decoder application.
This file contains all the important settings and API configurations.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Configuration class that holds all the settings for the application.
    """
    
    # Google Gemini API Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    GEMINI_MODEL = 'gemini-1.5-flash'  # You can change this to other Gemini models
    
    # Database Configuration
    DATABASE_PATH = 'database/label_decoder.db'
    
    # File Upload Configuration
    UPLOAD_FOLDER = 'uploads'
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
    
    # Streamlit Configuration
    PAGE_TITLE = "Label Decoder"
    PAGE_ICON = "📷"
    
    # Analysis Prompt for Gemini
    ANALYSIS_PROMPT = """
    You are an expert in analyzing product labels and ingredients. Please analyze this product label image and provide the following information:

    1. **Product Name**: What is the name of the product?
    2. **Brand**: What brand is this product from?
    3. **Product Type**: What type of product is this (e.g., food, cosmetic, medicine, etc.)?
    4. **Key Ingredients**: List the main ingredients found on the label
    5. **Nutritional Information**: If available, provide nutritional facts
    6. **Allergen Warnings**: Any allergen warnings or precautions mentioned
    7. **Health Analysis**: 
       - Are there any potentially harmful ingredients?
       - Overall health rating (1-10, where 10 is very healthy)
       - Recommendations for consumers
    8. **Additional Information**: Any other important details from the label

    Please be thorough and provide accurate information based on what you can see in the image.
    """

# Create an instance for easy importing
config = Config()
