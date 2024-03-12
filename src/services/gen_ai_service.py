from langchain import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import LLMMathChain
from langchain.tools import DuckDuckGoSearchRun
from langchain import hub
from langchain.agents import load_tools
from langchain.agents import initialize_agent, Tool
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent
from langchain.agents.agent_types import AgentType

from dotenv import load_dotenv
import os

load_dotenv()
api_key=os.getenv("OPENAI_API_KEY")

class GenAiService:
    async def generate_response(self, user_query):

        llm = OpenAI(
            openai_api_key=api_key,
            temperature=0
        )

        prompt = PromptTemplate(
            input_variables=["query"],
            template="{query}"
        )

        llm_chain = LLMChain(llm=llm, prompt=prompt)

        llm_math = LLMMathChain(llm=llm)

        search = DuckDuckGoSearchRun()

        tools=[
            Tool(
                name='Language Model',
                func=llm_chain.run,
                description='use this tool for general purpose queries'
            ),
            Tool(
                name='Calculator',
                func=llm_math.run,
                description='Useful for when you need to answer questions about math.'
            ),
            Tool(
                name="Search",
                func=search.run,
                description="useful for when you need to answer questions about current events",
            )
        ]


        # Load the "arxiv" tool
        arxiv_tool = load_tools(["arxiv"])

        # Add the loaded tool to your existing list
        tools.extend(arxiv_tool)


        prompt = hub.pull("hwchase17/react")

        memory = ConversationBufferMemory(memory_key="chat_history")


        conversational_agent = initialize_agent(
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            tools=tools,
            llm=llm,
            verbose=True,
            max_iterations=3,
            memory=memory,
        )


        output=conversational_agent.run(input=user_query)

        return output
       
