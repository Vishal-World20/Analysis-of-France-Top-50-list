"""
France Top 50 Playlist Analysis - Streamlit App Entry Point
This file serves as the main entry point for Streamlit Cloud deployment
"""
import os
import sys

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

# Import and run the main app
from app.streamlit_app import *
