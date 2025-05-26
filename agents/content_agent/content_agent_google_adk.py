"""Google ADK based content generation agent."""

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from config import settings
from .tools.research_tool import perform_web_research

# Expose the research function so the agent's LLM can invoke it when needed.
research_tool_adk = FunctionTool(
    fn=perform_web_research,
    name="ResearchTool",
    description="Performs web research for a given query and returns summaries of top results.",
)


class ContentAgentGoogleADK:
    """Agent capable of producing content using either Gemini or OpenAI models."""

    def __init__(self, model_name: str | None = None, use_openai_model: bool = False) -> None:
        llm_provider = None
        if use_openai_model:
            from google.adk.llms.litellm import LiteLlm
            llm_provider = LiteLlm(model=model_name or f"openai/{settings.DEFAULT_OPENAI_MODEL}")
        else:
            llm_provider = model_name or settings.DEFAULT_GOOGLE_GEMINI_MODEL

        self.agent = Agent(
            name="GoogleADKContentAgent",
            llm=llm_provider,
            instructions="You are a creative content writer. Use tools to research topics and analyze style.",
            tools=[research_tool_adk],
        )

    def generate_content(self, topic: str, content_type: str = "blog_post_outline") -> str:
        """Generate a piece of content using the configured ADK agent."""

        from google.adk.runners import Runner
        from google.adk.sessions.in_memory_session_service import InMemorySessionService

        session_service = InMemorySessionService()
        session = session_service.create_session(user_id="user123", app_name="ContentAgentApp")
        runner = Runner(app_name="ContentAgentApp", agent=self.agent, session_service=session_service)
        query = f"Create a {content_type} about {topic}."
        events = list(runner.run_once(session_id=session.session_id, query=query))
        final_response = "".join(
            e.content for e in events if e.type == "TEXT" and e.source.type == "MODEL"
        )
        return final_response
