# config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env file

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Google Cloud Settings
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")

# Example: Default models
DEFAULT_OPENAI_MODEL = "gpt-4o"
DEFAULT_GOOGLE_GEMINI_MODEL = "gemini-1.5-flash"

# You can add more project-specific configurations here
CRM_API_ENDPOINT = os.getenv("CRM_API_ENDPOINT")
CRM_API_KEY = os.getenv("CRM_API_KEY")

# Ensure critical keys are set
if not OPENAI_API_KEY:
    print("Warning: OPENAI_API_KEY not found in .env file.")
if not GOOGLE_CLOUD_PROJECT:
    print("Warning: GOOGLE_CLOUD_PROJECT not found in .env file.")
