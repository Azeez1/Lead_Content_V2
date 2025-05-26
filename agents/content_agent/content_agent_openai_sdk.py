"""Content creation agent built with the OpenAI Agents SDK."""

from openai_agents import Agent, Runner, function_tool
from config import settings
from .tools.research_tool import perform_web_research


@function_tool
def research_tool_openai(query: str, num_results: int = 3) -> list:
    """Simple research tool for the OpenAI agent."""

    return perform_web_research(query, num_results)


class ContentAgentOpenAISDK:
    def __init__(self, model_name: str = settings.DEFAULT_OPENAI_MODEL):
        """Initialize the content agent with the desired OpenAI model."""

        self.agent = Agent(
            name="OpenAIContentAgent",
            instructions="You are a creative content writer using OpenAI SDK.",
            model=model_name,
            tools=[research_tool_openai],
        )

    def generate_content(self, topic: str, content_type: str = "blog_post_outline"):
        """Generate content for the given topic."""

        query = f"Create a {content_type} about {topic}."
        result = Runner.run_sync(self.agent, query)
        return result.final_output
