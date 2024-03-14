from langchain import OpenAI
from sqlalchemy.orm import Session
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
from src.dao.user_dao import UserDAO
from sqlalchemy import MetaData
from langchain.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from src.config.database import engine



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
        db = SQLDatabase(engine)
        sql_chain = SQLDatabaseChain(llm = llm, database=db, verbose=True)

        metadat_obj = MetaData()

        sql_tool = Tool(
        name = 'RealEstate DB',
        func = sql_chain.run,
        description = "Useful when you need to answer the question about the RealEstate and its prices"
        )

        tools.append(sql_tool)
        # Load the "arxiv" tool
        arxiv_tool = load_tools(["arxiv"])

        # Add the loaded tool to your existing list
        tools.extend(arxiv_tool)


        prompt = hub.pull("hwchase17/react")

        memory = ConversationBufferMemory(memory_key="chat_history")

        previous_chats = await self.user_dao.fetch_previous_chat(user_id)
        for chat in previous_chats:
            memory.chat_memory.add_user_message(chat['question'])
            memory.chat_memory.add_ai_message(chat['answer'])
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
       
