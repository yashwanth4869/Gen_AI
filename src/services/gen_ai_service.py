from langchain import OpenAI
from sqlalchemy.orm import Session
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import LLMMathChain
from langchain.tools import DuckDuckGoSearchRun
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain import hub
from langchain.agents import load_tools
from langchain.agents import initialize_agent, Tool
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent
from langchain.agents.agent_types import AgentType
from src.dao.user_dao import UserDAO
from sqlalchemy import MetaData
from src.config.database import engine
from langchain_community.agent_toolkits import create_sql_agent
from src.config.database_initializer import get_db
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from src.services.sql_tool import SQLCustomTool
from src.services.csv_tool import CSVCustomTool


from dotenv import load_dotenv
import os
class GenAiService:
    def __init__(self, db: Session):

        self.user_dao = UserDAO(db)

    async def generate_response(self, user_query, user_id):
        

        load_dotenv()
        api_key=os.getenv("OPENAI_API_KEY")

        llm = OpenAI(
            openai_api_key=api_key,
            temperature=0
        )

        prompt = PromptTemplate(
            input_variables=["query"],
            template="{query}"
        )

        # prompt = hub.pull("hwchase17/react")

        # prompt_template = """Use the following as it is:"{text}"DO NOT SUMMARIZE:"""
        # PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])

        llm_chain = LLMChain(llm=llm, prompt=prompt)

        llm_math = LLMMathChain(llm=llm)
        search = DuckDuckGoSearchRun()

        # loader = CSVLoader(file_path='src/csat_resources_feedback 1.csv')
        # data = loader.load()
        # csv_file = 'src/csat_resources_feedback 1.csv'
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

        metadat_obj = MetaData()

        sql_tool = SQLCustomTool()
        csv_tool = CSVCustomTool()
        tools.append(sql_tool)
        tools.append(csv_tool)
        tools_list = list(tools)
        
        # Load the "arxiv" tool
        arxiv_tool = load_tools(["arxiv"])
        
        # Add the loaded tool to your existing list
        tools.extend(arxiv_tool)


        prompt = hub.pull("hwchase17/react")
        tools = sql_tool
        memory = ConversationBufferMemory(memory_key="chat_history")
        previous_chats = await self.user_dao.fetch_previous_chat(user_id)
        for chat in previous_chats:
            if chat['answer'] and not chat['answer'].startswith('Is there anything else'):
                memory.chat_memory.add_user_message(chat['question'])
                memory.chat_memory.add_ai_message(chat['answer'])


        # PREFIX = """Answer the following questions as best you can. You have access to the following tools:
        #             sql_tool, search tool, calculator tool, LLM tool, arxiv tool related to research papers"""
        # FORMAT_INSTRUCTIONS = """
        # Use the following format:


        # Question: the input question you must answer
        # Thought: you should always think about what to do
        # Action: the action to take, should be one of [{tool_names}]
        # Action Input: the input to the action
        # Observation: the result of the action
        # ... (this Thought/Action/Action Input/Observation can repeat N times)
        # Thought: I now know the final answer
        # Final Answer: the final answer to the original input question"""
        # SUFFIX = """Begin!"""

        conversational_agent = initialize_agent(
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            tools=tools_list,
            llm=llm,
            verbose=True,
            max_iterations=5,
            memory=memory,
            handle_parsing_errors=True,
            )


        output = conversational_agent.run(input=user_query)
        temp = output
        temp_query = user_query
        while(temp.startswith('Is there anything else')):
            temp_query = llm.invoke(input = f'reframe the sentence : {user_query}')
            temp = conversational_agent.run(input=temp_query)

        # print('****************************', output)
        # print('****************************', temp)
        
        return temp


