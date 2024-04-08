from langchain import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import LLMMathChain
from langchain import hub
from langchain.agents import initialize_agent, Tool, load_tools
from langchain.memory import ConversationBufferMemory
from langchain.agents.agent_types import AgentType
from src.dao.user_dao import UserDAO
from src.services.sql_services.sql_chain_tool2 import SQLCustomTool
from src.services.csv_tool import CSVCustomTool
from langchain_community.chat_message_histories.upstash_redis import UpstashRedisChatMessageHistory
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session
import uuid

class SQLQueryService2:
    def __init__(self, db: Session):
        self.user_dao = UserDAO(db)

    async def generate_sql_query_response(self, request, user_id, session_id):

        data = await request.json()
        user_query = data.get('user', None)
        # data_base = data.get('db_id',1)

        if session_id == 'undefined':
            session_id=str(uuid.uuid4())
        
        load_dotenv()
        api_key=os.getenv("OPENAI_API_KEY")
        user_query = user_query + " from the given real estate database. Strictly dont tell me anything like- 'Is there anything else you would like to know'. I strictly want you to Give me the final answer which is present in your 'observation'. *Strictly Give me the final result. I dont want you to tell 'Is there anything else I can assist you with?'"
        llm = OpenAI(
            openai_api_key=api_key,
            temperature=0
        )

        chain_prompt = PromptTemplate(
            input_variables=["query"],
            template="{query}"
        )

        history = UpstashRedisChatMessageHistory(
            url = os.getenv("REDIS_URL"),
            token = os.getenv("REDIS_TOKEN"),
            session_id = session_id,
        )

        memory = ConversationBufferMemory(
            memory_key = "chat_history",
            return_messages = True,
            chat_memory = history
        )

        llm_chain = LLMChain(llm=llm, prompt=chain_prompt)
        llm_math = LLMMathChain(llm=llm)

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
        ]

        sql_tool = SQLCustomTool()
        
        tools.append(sql_tool)

        # csv_tool=CSVCustomTool()
        # tools.append(csv_tool)

        # rag_tool = RagCustomTool()
        # tools.append(rag_tool)

        # # Load the "arxiv" tool
        # arxiv_tool = load_tools(["arxiv"])

        # # Add the loaded tool to your existing list
        # tools.extend(arxiv_tool)


        prompt = hub.pull("hwchase17/openai-functions-agent")

        # memory = ConversationBufferMemory(memory_key="chat_history")


        conversational_agent = initialize_agent(
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            tools=tools,
            llm=llm,
            verbose=True,
            max_iterations=3,
            prompt=prompt,
            memory=memory,
        )


        output=conversational_agent.run(input=user_query)
        return {'bot': output, 'session_id':session_id}
       
