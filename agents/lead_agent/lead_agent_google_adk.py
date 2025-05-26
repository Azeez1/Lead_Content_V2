"""Implementation of the lead generation agent using Google ADK."""

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from config import settings
from .tools.web_prospector import prospect_website


# ---------------------------------------------------------------------------
# Tool definitions
# ---------------------------------------------------------------------------
# ``FunctionTool`` wraps a plain Python function so that it can be invoked by an
# ADK agent when the LLM determines that tool usage is required.
web_prospector_adk_tool = FunctionTool(
    fn=prospect_website,
    name="WebProspector",
    description="Scrapes a website URL to find potential lead information like company title and emails.",
)


class LeadAgentGoogleADK:
    """Lead generation agent built with the Google Agent Development Kit."""

    def __init__(self, model_name: str | None = None, use_openai_model: bool = False) -> None:
        """Create the agent and configure the underlying language model."""

        llm_provider = None
        if use_openai_model:
            # The ADK can use OpenAI models via LiteLLM.  This is helpful if you
            # prefer OpenAI's models but still want to build your agent in the
            # ADK framework.
            from google.adk.llms.litellm import LiteLlm

            llm_provider = LiteLlm(model=model_name or f"openai/{settings.DEFAULT_OPENAI_MODEL}")
            print(
                f"Google ADK Agent configured to attempt using OpenAI model: {model_name or settings.DEFAULT_OPENAI_MODEL} via LiteLLM"
            )
        else:
            # Default to using one of the Gemini models on Google Cloud.
            llm_provider = model_name or settings.DEFAULT_GOOGLE_GEMINI_MODEL
            print(f"Google ADK Agent configured with Google model: {llm_provider}")

        # ------------------------------------------------------------------
        # Construct the ADK Agent
        # ------------------------------------------------------------------
        self.agent = Agent(
            name="GoogleADKLeadAgent",
            llm=llm_provider,
            instructions=(
                "You are a lead generation specialist. Your goal is to identify and qualify potential leads. "
                "Use available tools to research companies and individuals. "
                "Provide a structured summary of your findings, including contact information, company details, "
                "and an initial qualification assessment based on predefined criteria (e.g., company size, industry)."
            ),
            tools=[web_prospector_adk_tool],
        )
        print("LeadAgentGoogleADK initialized.")

    def process_lead_request(self, task_description: str, user_id: str = "user123", session_id: str | None = None):
        """Run the agent for a single lead generation task."""

        from google.adk.runners import Runner
        from google.adk.sessions.in_memory_session_service import InMemorySessionService

        # Session service manages conversational state between invocations.
        session_service = InMemorySessionService()
        if session_id:
            session = session_service.get_session(user_id=user_id, session_id=session_id)
            if not session:
                session = session_service.create_session(user_id=user_id, session_id=session_id, app_name="LeadAgentApp")
        else:
            session = session_service.create_session(user_id=user_id, app_name="LeadAgentApp")
            session_id = session.session_id

        runner = Runner(app_name="LeadAgentApp", agent=self.agent, session_service=session_service)

        print(f"\nProcessing lead request with Google ADK Agent (Session: {session_id}): '{task_description}'")
        try:
            response_events = list(runner.run_once(session_id=session_id, query=task_description))
            final_response = ""
            for event in response_events:
                if event.type == "TEXT" and event.source.type == "MODEL":
                    final_response += event.content
                elif event.type == "TOOL_CALL":
                    print(f"  ADK Tool call requested: {event.tool_name} with args {event.tool_input}")
                elif event.type == "TOOL_OUTPUT":
                    print(f"  ADK Tool output received for {event.tool_name}")
            print(f"Google ADK Agent final response:\n{final_response}")
            return final_response, session_id
        except Exception as e:  # pragma: no cover - runtime diagnostics
            print(f"Error processing with Google ADK Agent: {e}")
            return f"Error: {e}", session_id


if __name__ == '__main__':
    adk_lead_agent_with_openai = LeadAgentGoogleADK(use_openai_model=True, model_name="gpt-4o")
    task2 = "Prospect the website 'https://www.example.com' for company information and contact emails."
    response2, sid2 = adk_lead_agent_with_openai.process_lead_request(task2)
