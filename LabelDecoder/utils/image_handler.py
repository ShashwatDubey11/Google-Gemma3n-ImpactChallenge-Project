"""
Image utility functions for the Label Decoder application.
This module handles image processing, validation, and file operations.
"""

import os
import uuid
from PIL import Image
import streamlit as st
from typing import Tuple, Optional
import hashlib
import datetime

class ImageHandler:
    """
    Handles all image-related operations including validation, processing, and storage.
    """
    
    def __init__(self, upload_folder: str = "uploads"):
        """
        Initialize the image handler.
        
        Args:
            upload_folder (str): Directory where images will be stored
        """
        self.upload_folder = upload_folder
        self.ensure_upload_folder_exists()
    
    def ensure_upload_folder_exists(self):
        """Create the upload folder if it doesn't exist."""
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder, exist_ok=True)
    
    def validate_image(self, uploaded_file) -> Tuple[bool, str]:
        """
        Validate the uploaded image file.
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if uploaded_file is None:
            return False, "No file uploaded"
        
        # Check file size (10MB limit)
        max_size = 10 * 1024 * 1024  # 10MB
        if uploaded_file.size > max_size:
            return False, f"File size too large. Maximum allowed: {max_size // (1024*1024)}MB"
        
        # Check file extension
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
        file_extension = uploaded_file.name.split('.')[-1].lower() if '.' in uploaded_file.name else ''
        
        if file_extension not in allowed_extensions:
            return False, f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
        
        # Try to open the image to verify it's a valid image file
        try:
            image = Image.open(uploaded_file)
            image.verify()
            return True, "Valid image"
        except Exception as e:
            return False, f"Invalid image file: {str(e)}"
    
    def generate_unique_filename(self, original_filename: str) -> str:
        """
        Generate a unique filename for the uploaded image.
        
        Args:
            original_filename (str): Original filename from user
            
        Returns:
            str: Unique filename
        """
        # Get file extension
        file_extension = original_filename.split('.')[-1].lower() if '.' in original_filename else 'jpg'
        
        # Generate unique identifier
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        
        # Create unique filename
        unique_filename = f"label_{timestamp}_{unique_id}.{file_extension}"
        
        return unique_filename
    
    def save_uploaded_image(self, uploaded_file, custom_filename: str = None) -> Tuple[bool, str, dict]:
        """
        Save the uploaded image to the filesystem.
        
        Args:
            uploaded_file: Streamlit uploaded file object
            custom_filename (str): Custom filename (optional)
            
        Returns:
            Tuple[bool, str, dict]: (success, message, file_info)
        """
        try:
            # Validate the image first
            is_valid, validation_message = self.validate_image(uploaded_file)
            if not is_valid:
                return False, validation_message, {}
            
            # Generate filename
            if custom_filename:
                filename = custom_filename
            else:
                filename = self.generate_unique_filename(uploaded_file.name)
            
            # Create full file path
            file_path = os.path.join(self.upload_folder, filename)
            
            # Reset file pointer to beginning
            uploaded_file.seek(0)
            
            # Save the file
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Get file information
            file_info = {
                'filename': filename,
                'original_filename': uploaded_file.name,
                'file_path': file_path,
                'file_size': uploaded_file.size,
                'content_type': uploaded_file.type if hasattr(uploaded_file, 'type') else 'image/*'
            }
            
            return True, f"Image saved successfully as {filename}", file_info
            
        except Exception as e:
            return False, f"Error saving image: {str(e)}", {}
    
    def get_image_info(self, image_path: str) -> Optional[dict]:
        """
        Get information about an image file.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            dict or None: Image information
        """
        try:
            if not os.path.exists(image_path):
                return None
            
            # Open image to get dimensions
            with Image.open(image_path) as img:
                width, height = img.size
                format_name = img.format
                mode = img.mode
            
            # Get file size
            file_size = os.path.getsize(image_path)
            
            return {
                'path': image_path,
                'width': width,
                'height': height,
                'format': format_name,
                'mode': mode,
                'size_bytes': file_size,
                'size_mb': round(file_size / (1024 * 1024), 2)
            }
            
        except Exception as e:
            st.error(f"Error getting image info: {str(e)}")
            return None
    
    def resize_image_if_needed(self, image_path: str, max_width: int = 1024, max_height: int = 1024) -> bool:
        """
        Resize image if it's too large for processing.
        
        Args:
            image_path (str): Path to the image file
            max_width (int): Maximum width
            max_height (int): Maximum height
            
        Returns:
            bool: True if image was resized, False otherwise
        """
        try:
            with Image.open(image_path) as img:
                original_size = img.size
                
                # Check if resize is needed
                if img.width <= max_width and img.height <= max_height:
                    return False
                
                # Calculate new size maintaining aspect ratio
                ratio = min(max_width / img.width, max_height / img.height)
                new_size = (int(img.width * ratio), int(img.height * ratio))
                
                # Resize and save
                resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
                resized_img.save(image_path)
                
                return True
                
        except Exception as e:
            st.error(f"Error resizing image: {str(e)}")
            return False
    
    def generate_thumbnail(self, image_path: str, thumb_size: Tuple[int, int] = (200, 200)) -> Optional[str]:
        """
        Generate a thumbnail for the image.
        
        Args:
            image_path (str): Path to the original image
            thumb_size (Tuple[int, int]): Thumbnail size (width, height)
            
        Returns:
            str or None: Path to the thumbnail or None if failed
        """
        try:
            # Create thumbnail filename
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            thumb_filename = f"{base_name}_thumb.jpg"
            thumb_path = os.path.join(self.upload_folder, "thumbnails", thumb_filename)
            
            # Create thumbnails directory
            thumb_dir = os.path.dirname(thumb_path)
            if not os.path.exists(thumb_dir):
                os.makedirs(thumb_dir, exist_ok=True)
            
            # Generate thumbnail
            with Image.open(image_path) as img:
                img.thumbnail(thumb_size, Image.Resampling.LANCZOS)
                img.save(thumb_path, "JPEG")
            
            return thumb_path
            
        except Exception as e:
            st.error(f"Error generating thumbnail: {str(e)}")
            return None
    
    def delete_image(self, image_path: str) -> bool:
        """
        Delete an image file.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            bool: True if deleted successfully, False otherwise
        """
        try:
            if os.path.exists(image_path):
                os.remove(image_path)
                return True
            return False
        except Exception as e:
            st.error(f"Error deleting image: {str(e)}")
            return False

# Create a global instance for easy importing
image_handler = ImageHandler()
