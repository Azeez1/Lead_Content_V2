# agents/lead_agent/lead_agent_openai_sdk.py
from openai_agents import Agent, Runner, function_tool, ModelSettings
from config import settings
from .tools.web_prospector import prospect_website


@function_tool
def web_prospector_openai_tool(url: str) -> dict:
    """
    Scrapes a given website URL to find potential lead information such as company title and email addresses.
    Use this tool to research a specific company's website.
    Args:
        url (str): The URL of the website to scrape.
    Returns:
        dict: A dictionary containing extracted information (title, emails) or an error message.
    """
    return prospect_website(url)


class LeadAgentOpenAISDK:
    def __init__(self, model_name: str = settings.DEFAULT_OPENAI_MODEL):
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY must be set in the environment.")

        self.agent = Agent(
            name="OpenAILeadAgent",
            instructions=(
                "You are a highly efficient lead generation specialist. Your primary goal is to identify, "
                "research, and qualify potential leads based on the user's request. "
                "Utilize the available tools to gather information from websites and CRMs. "
                "Present your findings in a structured summary, including company details, "
                "key contacts, email addresses found, and a brief qualification assessment. "
                "If a website URL is provided, always use the web_prospector_openai_tool to investigate it first."
            ),
            model=model_name,
            tools=[
                web_prospector_openai_tool,
            ],
        )
        print(f"LeadAgentOpenAISDK initialized with model: {model_name}")

    def process_lead_request(self, task_description: str):
        print(f"\nProcessing lead request with OpenAI SDK Agent: '{task_description}'")
        try:
            result = Runner.run_sync(self.agent, task_description)
            final_output = result.final_output
            if isinstance(final_output, dict) and "error" in final_output:
                print(f"  OpenAI Tool execution might have resulted in an error: {final_output}")
            elif result.run_context and result.run_context.history:
                print("  OpenAI Agent execution trace:")
                for msg in result.run_context.history:
                    if msg.role == "tool":
                        print(f"    Tool: {msg.name}, Args: {msg.tool_calls[0].function.arguments if msg.tool_calls else 'N/A'}")
                        print(f"    Tool Output: {msg.tool_calls[0].function.output if msg.tool_calls else 'N/A'}")
                    else:
                        print(f"    {msg.role.capitalize()}: {msg.content}")
            print(f"OpenAI SDK Agent final response:\n{final_output}")
            return final_output
        except Exception as e:
            print(f"Error processing with OpenAI SDK Agent: {e}")
            return f"Error: {e}"


if __name__ == '__main__':
    openai_lead_agent = LeadAgentOpenAISDK()
    task2 = "Can you prospect the website 'https://www.example.com' and tell me what you find?"
    response2 = openai_lead_agent.process_lead_request(task2)
