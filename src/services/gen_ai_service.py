from langchain.agents import initialize_agent
from langchain.agents.agent_types import AgentType
from src.utlis.agent_executor import con as conversational_agent
class GenAiService:
    async def generate_response(self, user_query):

        output=conversational_agent.run(input=user_query)

        return output
       
