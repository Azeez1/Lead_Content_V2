# main.py
from config import settings
from agents.lead_agent.lead_agent_google_adk import LeadAgentGoogleADK
from agents.lead_agent.lead_agent_openai_sdk import LeadAgentOpenAISDK
from agents.content_agent.content_agent_google_adk import ContentAgentGoogleADK
from agents.content_agent.content_agent_openai_sdk import ContentAgentOpenAISDK


def run_lead_generation_tasks():
    print("--- Running Lead Generation Tasks ---")
    print("\nInitializing Lead Agent with OpenAI SDK...")
    lead_agent_o = LeadAgentOpenAISDK(model_name=settings.DEFAULT_OPENAI_MODEL)
    response_o1 = lead_agent_o.process_lead_request(
        "Can you look up information on 'Innovate Corp' by prospecting their website 'https://www.innovatecorp.com' (mock URL, use example.com)?"
    )
    print(f"Lead Agent (OpenAI SDK) Response for Innovate Corp: {response_o1}")


def run_content_generation_tasks():
    print("\n--- Running Content Generation Tasks ---")
    pass


if __name__ == "__main__":
    print("AI Agent Project Initializing...")
    if not settings.OPENAI_API_KEY and not settings.GOOGLE_APPLICATION_CREDENTIALS:
        print("CRITICAL ERROR: Neither OpenAI nor Google Cloud credentials are set. Agents may not function.")
        exit(1)
    elif not settings.OPENAI_API_KEY:
        print("Warning: OPENAI_API_KEY is not set. OpenAI SDK agents or ADK with OpenAI models will fail.")
    elif not settings.GOOGLE_APPLICATION_CREDENTIALS and not settings.GOOGLE_CLOUD_PROJECT:
        print("Warning: Google Cloud credentials/project not set. Google ADK agents with Google models may fail.")

    run_lead_generation_tasks()
    print("\nAI Agent Project Tasks Complete.")
