"""
Database module for storing uploaded images and analysis results.
This module handles all database operations using SQLite.
"""

import sqlite3
import os
import datetime
from typing import Optional, List, Dict
import json

class DatabaseManager:
    """
    Manages all database operations for the Label Decoder application.
    Uses SQLite database to store image information and analysis results.
    """
    
    def __init__(self, db_path: str = "database/label_decoder.db"):
        """
        Initialize the database manager.
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db_path = db_path
        self.ensure_database_exists()
        self.create_tables()
    
    def ensure_database_exists(self):
        """Create the database directory if it doesn't exist."""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
    
    def get_connection(self):
        """Get a database connection."""
        return sqlite3.connect(self.db_path)
    
    def create_tables(self):
        """
        Create the necessary tables in the database.
        This includes tables for storing image uploads and analysis results.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Table for storing uploaded images
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS uploaded_images (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    original_filename TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    file_size INTEGER,
                    upload_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    analysis_status TEXT DEFAULT 'pending'
                )
            ''')
            
            # Table for storing analysis results
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS analysis_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    image_id INTEGER,
                    analysis_text TEXT,
                    analysis_json TEXT,
                    analysis_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    model_used TEXT,
                    FOREIGN KEY (image_id) REFERENCES uploaded_images (id)
                )
            ''')
            
            conn.commit()
    
    def save_uploaded_image(self, filename: str, original_filename: str, 
                          file_path: str, file_size: int) -> int:
        """
        Save information about an uploaded image to the database.
        
        Args:
            filename (str): Generated filename for the image
            original_filename (str): Original filename from user
            file_path (str): Path where the image is stored
            file_size (int): Size of the image file in bytes
            
        Returns:
            int: The ID of the inserted record
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO uploaded_images 
                (filename, original_filename, file_path, file_size)
                VALUES (?, ?, ?, ?)
            ''', (filename, original_filename, file_path, file_size))
            
            conn.commit()
            return cursor.lastrowid
    
    def save_analysis_result(self, image_id: int, analysis_text: str, 
                           analysis_json: str, model_used: str) -> int:
        """
        Save the analysis result for an image.
        
        Args:
            image_id (int): ID of the image that was analyzed
            analysis_text (str): Raw text response from the AI model
            analysis_json (str): Structured JSON response (if available)
            model_used (str): Name of the AI model used for analysis
            
        Returns:
            int: The ID of the inserted analysis record
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO analysis_results 
                (image_id, analysis_text, analysis_json, model_used)
                VALUES (?, ?, ?, ?)
            ''', (image_id, analysis_text, analysis_json, model_used))
            
            # Update the image status
            cursor.execute('''
                UPDATE uploaded_images 
                SET analysis_status = 'completed'
                WHERE id = ?
            ''', (image_id,))
            
            conn.commit()
            return cursor.lastrowid
    
    def get_image_by_id(self, image_id: int) -> Optional[Dict]:
        """
        Get image information by ID.
        
        Args:
            image_id (int): ID of the image
            
        Returns:
            Dict or None: Image information dictionary
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM uploaded_images WHERE id = ?
            ''', (image_id,))
            
            row = cursor.fetchone()
            if row:
                columns = [description[0] for description in cursor.description]
                return dict(zip(columns, row))
            return None
    
    def get_analysis_by_image_id(self, image_id: int) -> Optional[Dict]:
        """
        Get analysis result for an image.
        
        Args:
            image_id (int): ID of the image
            
        Returns:
            Dict or None: Analysis result dictionary
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM analysis_results WHERE image_id = ?
                ORDER BY analysis_timestamp DESC LIMIT 1
            ''', (image_id,))
            
            row = cursor.fetchone()
            if row:
                columns = [description[0] for description in cursor.description]
                return dict(zip(columns, row))
            return None
    
    def get_recent_uploads(self, limit: int = 10) -> List[Dict]:
        """
        Get recent uploaded images.
        
        Args:
            limit (int): Maximum number of records to return
            
        Returns:
            List[Dict]: List of image dictionaries
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM uploaded_images 
                ORDER BY upload_timestamp DESC 
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
    
    def get_upload_statistics(self) -> Dict:
        """
        Get statistics about uploads and analyses.
        
        Returns:
            Dict: Statistics dictionary
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Total uploads
            cursor.execute('SELECT COUNT(*) FROM uploaded_images')
            total_uploads = cursor.fetchone()[0]
            
            # Completed analyses
            cursor.execute("SELECT COUNT(*) FROM uploaded_images WHERE analysis_status = 'completed'")
            completed_analyses = cursor.fetchone()[0]
            
            # Pending analyses
            cursor.execute("SELECT COUNT(*) FROM uploaded_images WHERE analysis_status = 'pending'")
            pending_analyses = cursor.fetchone()[0]
            
            return {
                'total_uploads': total_uploads,
                'completed_analyses': completed_analyses,
                'pending_analyses': pending_analyses
            }

# Create a global instance for easy importing
db_manager = DatabaseManager()
