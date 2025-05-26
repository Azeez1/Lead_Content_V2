"""Helpers for configuring alternative language models."""

from google.adk.llms.litellm import LiteLlm  # LiteLLM adapter available in ADK
from config import settings


def get_openai_llm_for_adk(model_name: str = settings.DEFAULT_OPENAI_MODEL) -> LiteLlm | None:
    """Return a LiteLlm instance configured for an OpenAI model.

    The Google ADK natively supports Gemini models.  To use OpenAI models within
    the ADK framework we rely on LiteLLM which acts as a universal adapter.  This
    function constructs the ``LiteLlm`` object for the requested ``model_name``.

    Parameters
    ----------
    model_name:
        Name of the OpenAI model to use (e.g. ``"gpt-4o"``).  If omitted, the
        default specified in :mod:`config.settings` is used.

    Returns
    -------
    LiteLlm | None
        The configured ``LiteLlm`` instance, or ``None`` if configuration fails.
    """

    # Ensure an API key is present.  Without it, LiteLLM cannot contact the
    # OpenAI service.
    if not settings.OPENAI_API_KEY:
        raise ValueError(
            "OPENAI_API_KEY must be set in the environment for this provider."
        )

    try:
        # Instantiating ``LiteLlm`` with the model name is often sufficient.  It
        # will pick up the API key from the environment variables.
        llm = LiteLlm(model=model_name)
        print(f"Configured LiteLlm for ADK with model: {model_name}")
        return llm
    except Exception as e:  # pragma: no cover - defensive
        # Any error here is likely due to misconfiguration of LiteLLM or missing
        # dependencies.
        print(f"Error configuring LiteLlm for ADK: {e}")
        print("Make sure 'litellm' is installed and OPENAI_API_KEY is set.")
        return None

