"""
Google Gemini API integration for analyzing product labels.
This module handles all interactions with Google's Gemini AI model.
"""

import google.generativeai as genai
from PIL import Image
import os
import logging
from typing import Optional, Dict, Any, List
import json
import streamlit as st

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiAnalyzer:
    """
    Handles integration with Google Gemini AI for image analysis.
    """
    
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        """
        Initialize the Gemini analyzer.
        
        Args:
            api_key (str): Google Gemini API key
            model_name (str): Name of the Gemini model to use
        """
        self.api_key = api_key
        self.model_name = model_name
        self.model = None
        
        if self.api_key:
            self.configure_api()
        else:
            logger.warning("No API key provided. Gemini analysis will not be available.")
    
    def configure_api(self):
        """Configure the Google Generative AI API."""
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
            logger.info(f"Gemini API configured successfully with model: {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to configure Gemini API: {str(e)}")
            self.model = None
    
    def is_configured(self) -> bool:
        """Check if the API is properly configured."""
        return self.model is not None
    
    def analyze_label_image(self, image_path: str, custom_prompt: str = None) -> Dict[str, Any]:
        """
        Analyze a product label image using Gemini AI.
        
        Args:
            image_path (str): Path to the image file
            custom_prompt (str): Custom prompt for analysis (optional)
            
        Returns:
            Dict: Analysis result containing success status and data
        """
        if not self.is_configured():
            return {
                'success': False,
                'error': 'Gemini API is not configured. Please check your API key.',
                'data': None
            }
        
        try:
            # Load and validate the image
            if not os.path.exists(image_path):
                return {
                    'success': False,
                    'error': f'Image file not found: {image_path}',
                    'data': None
                }
            
            # Open the image
            image = Image.open(image_path)
            
            # Use default prompt if none provided
            if custom_prompt is None:
                custom_prompt = self._get_default_prompt()
            
            # Generate content using Gemini
            response = self.model.generate_content([custom_prompt, image])
            
            # Process the response
            if response.text:
                analysis_result = {
                    'raw_text': response.text,
                    'model_used': self.model_name,
                    'image_path': image_path,
                    'processed_data': self._process_response(response.text)
                }
                
                return {
                    'success': True,
                    'error': None,
                    'data': analysis_result
                }
            else:
                return {
                    'success': False,
                    'error': 'No response received from Gemini model',
                    'data': None
                }
                
        except Exception as e:
            logger.error(f"Error analyzing image with Gemini: {str(e)}")
            return {
                'success': False,
                'error': f'Analysis failed: {str(e)}',
                'data': None
            }
    
    def _get_default_prompt(self) -> str:
        """Get the default analysis prompt."""
        return """
        You are an expert in analyzing product labels and ingredients. Please analyze this product label image and provide the following information in a clear, structured format:

        **PRODUCT INFORMATION:**
        - Product Name: 
        - Brand: 
        - Product Type: (food, cosmetic, medicine, etc.)
        - Net Weight/Volume: 

        **INGREDIENTS ANALYSIS:**
        - Main Ingredients: (list the first 5-10 ingredients)
        - Preservatives: (if any)
        - Artificial Additives: (colors, flavors, etc.)
        - Natural vs Synthetic: (percentage estimate)

        **NUTRITIONAL INFORMATION:** (if available)
        - Calories per serving:
        - Key nutrients:
        - Serving size:

        **HEALTH & SAFETY:**
        - Allergen Warnings: 
        - Health Rating: (1-10, where 10 is very healthy)
        - Potential Concerns: (harmful ingredients, high sodium, etc.)
        - Recommendations: (who should avoid, moderation advice)

        **ADDITIONAL DETAILS:**
        - Expiry/Best Before: (if visible)
        - Manufacturing Details: (if visible)
        - Certifications: (organic, FDA approved, etc.)
        - Storage Instructions: (if visible)

        Please be thorough and accurate based on what you can clearly see in the image. If certain information is not visible or unclear, please mention that explicitly.
        """
    
    def _process_response(self, response_text: str) -> Dict[str, Any]:
        """
        Process the raw response text into structured data.
        
        Args:
            response_text (str): Raw response from Gemini
            
        Returns:
            Dict: Processed and structured data
        """
        # This is a simple processing function
        # You can enhance this to extract specific information
        # and structure it better
        
        processed = {
            'summary': self._extract_summary(response_text),
            'health_rating': self._extract_health_rating(response_text),
            'key_ingredients': self._extract_ingredients(response_text),
            'warnings': self._extract_warnings(response_text)
        }
        
        return processed
    
    def _extract_summary(self, text: str) -> str:
        """Extract a summary from the response."""
        lines = text.split('\n')
        # Take first few meaningful lines as summary
        summary_lines = []
        for line in lines[:3]:
            if line.strip() and not line.startswith('#'):
                summary_lines.append(line.strip())
        return ' '.join(summary_lines)[:200] + '...' if summary_lines else "Analysis completed"
    
    def _extract_health_rating(self, text: str) -> Optional[int]:
        """Extract health rating from the response."""
        import re
        # Look for patterns like "Health Rating: 7/10" or "Rating: 8"
        patterns = [
            r'Health Rating[:\s]+(\d+)',
            r'Rating[:\s]+(\d+)',
            r'(\d+)/10',
            r'(\d+)\s*out\s*of\s*10'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    rating = int(match.group(1))
                    if 1 <= rating <= 10:
                        return rating
                except ValueError:
                    continue
        return None
    
    def _extract_ingredients(self, text: str) -> List[str]:
        """Extract key ingredients from the response."""
        ingredients = []
        lines = text.split('\n')
        
        for line in lines:
            if 'ingredient' in line.lower() and ':' in line:
                # Extract ingredients after the colon
                parts = line.split(':', 1)
                if len(parts) > 1:
                    ingredient_text = parts[1].strip()
                    # Split by commas and clean up
                    items = [item.strip() for item in ingredient_text.split(',')]
                    ingredients.extend(items[:5])  # Take first 5
                    break
        
        return ingredients
    
    def _extract_warnings(self, text: str) -> List[str]:
        """Extract warnings from the response."""
        warnings = []
        lines = text.split('\n')
        
        warning_keywords = ['warning', 'allergen', 'caution', 'avoid', 'concern']
        
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in warning_keywords):
                if ':' in line:
                    warning_text = line.split(':', 1)[1].strip()
                    if warning_text:
                        warnings.append(warning_text)
                else:
                    warnings.append(line.strip())
        
        return warnings[:3]  # Return top 3 warnings

# Function to create analyzer instance
def create_gemini_analyzer(api_key: str) -> GeminiAnalyzer:
    """
    Create and return a GeminiAnalyzer instance.
    
    Args:
        api_key (str): Google Gemini API key
        
    Returns:
        GeminiAnalyzer: Configured analyzer instance
    """
    return GeminiAnalyzer(api_key)
