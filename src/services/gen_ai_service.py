from langchain import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import LLMMathChain
from langchain import hub
from langchain.agents import load_tools, initialize_agent, Tool
from langchain.memory import ConversationBufferMemory
from langchain.agents.agent_types import AgentType
from langchain_community.utilities import GoogleSerperAPIWrapper

from dotenv import load_dotenv
import os

load_dotenv()
api_key1 = os.getenv("OPENAI_API_KEY")
os.environ["SERPAPI_API_KEY"] = os.getenv("SERPAPI_API_KEY")

class GenAiService:
    async def generate_response(self, user_query):

        llm = OpenAI(
            openai_api_key=api_key1,
            temperature=0
        )

        prompt = PromptTemplate(
            input_variables=["query"],
            template="{query}"
        )

        llm_chain = LLMChain(llm=llm, prompt=prompt)

        llm_math = LLMMathChain(llm=llm)


        tools = [
            Tool(
                name='Language Model',
                func=llm_chain.run,
                description='use this tool for general purpose queries'
            ),
            Tool(
                name='Calculator',
                func=llm_math.run,
                description='Useful for when you need to answer questions about math.'
            )
        ]

        tools_names = ["serpapi"]
        serpapi_tool = load_tools(tool_names=tools_names,llm=llm)

        # Load the "arxiv" tool
        arxiv_tool = load_tools(["arxiv"])

        # Add the loaded tool to your existing list
        tools.extend(arxiv_tool)
        tools.extend(serpapi_tool)


        prompt = hub.pull("hwchase17/react")

        memory = ConversationBufferMemory(memory_key="chat_history")


        conversational_agent = initialize_agent(
            agent = AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            tools=tools,
            llm=llm,
            verbose=True,
            max_iterations=3,
            memory=memory,
        )


        output = conversational_agent.run(input=user_query)

        return output