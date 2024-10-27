"""

This module contains configuration settings for the FastAPI application.

"""

from dotenv import load_dotenv
import os
import json

# Load variables from .env file into environment
load_dotenv(
    dotenv_path="./app/.env",
    verbose=True
)

class Config:
    """Configuration settings for the FastAPI application."""

    # Debug mode: Enables detailed error messages and automatic reloading
    DEBUG = True
    
