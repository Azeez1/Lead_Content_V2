# hybrid_components/llm_providers.py
from google.adk.llms.litellm import LiteLlm  # If using LiteLLM with ADK
from config import settings


def get_openai_llm_for_adk(model_name: str = settings.DEFAULT_OPENAI_MODEL):
    """
    Configures an OpenAI model to be used within the Google ADK framework,
    typically via LiteLLM.
    Ensure OPENAI_API_KEY is set in your environment.
    """
    if not settings.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY must be set in the environment for this provider.")

    try:
        llm = LiteLlm(model=model_name)
        print(f"Configured LiteLlm for ADK with model: {model_name}")
        return llm
    except Exception as e:
        print(f"Error configuring LiteLlm for ADK: {e}")
        print("Make sure 'litellm' is installed and OPENAI_API_KEY is set.")
        return None
