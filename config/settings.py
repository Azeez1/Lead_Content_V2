"""Configuration loader for environment variables.

This module centralizes the reading of all environment variables needed
throughout the project.  The intention is to keep the logic for loading
settings in one place so that the rest of the code base simply imports the
values it requires.

Environment variables are loaded from a local ``.env`` file via
``python-dotenv``.  For sensitive values (API keys, project identifiers,
database credentials, etc.) ensure that ``config/.env`` is excluded from
version control.  See the provided ``.gitignore``.
"""

import os
from dotenv import load_dotenv


# ---------------------------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------------------------
# ``load_dotenv`` will read variables from ``config/.env`` if it exists and
# populate ``os.environ`` so ``os.getenv`` can retrieve them.  This keeps the
# API keys and configuration values outside of the code base.
load_dotenv()

# ---------------------------------------------------------------------------
# API Keys and Service Configuration
# ---------------------------------------------------------------------------

# OpenAI configuration -------------------------------------------------------
# The API key is required for any interaction with OpenAI models either via
# the OpenAI SDK directly or through LiteLLM when used from Google ADK.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Google Cloud configuration -------------------------------------------------
# ``GOOGLE_APPLICATION_CREDENTIALS`` should point to a service account JSON
# key file if the default credentials are not sufficient.
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
# The project and location identify the Google Cloud project and region for
# Gemini models or other services used by the ADK.
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")

# Default model names -------------------------------------------------------
# These defaults can be overridden when constructing agents, but keeping them
# here ensures a single place to change preferred models.
DEFAULT_OPENAI_MODEL = "gpt-4o"
DEFAULT_GOOGLE_GEMINI_MODEL = "gemini-1.5-flash"

# Additional configuration values can be defined below.  These are optional
# and depend entirely on how you extend the agents and their tools.
CRM_API_ENDPOINT = os.getenv("CRM_API_ENDPOINT")
CRM_API_KEY = os.getenv("CRM_API_KEY")


# ---------------------------------------------------------------------------
# Simple validation / warnings
# ---------------------------------------------------------------------------
# If essential keys are missing, print warnings so the developer is aware when
# running the code.  You could also raise exceptions here for stricter
# enforcement if desired.
if not OPENAI_API_KEY:
    print("Warning: OPENAI_API_KEY not found in .env file.")
if not GOOGLE_CLOUD_PROJECT:
    print("Warning: GOOGLE_CLOUD_PROJECT not found in .env file.")

