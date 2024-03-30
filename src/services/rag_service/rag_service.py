import os
from dotenv import load_dotenv
from langchain import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import LLMMathChain
from langchain.tools import DuckDuckGoSearchRun
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain import hub
from langchain.agents import initialize_agent, Tool, load_tools
from langchain.memory import ConversationBufferMemory
from langchain.agents.agent_types import AgentType
from src.dao.user_dao import UserDAO
from src.services.sql_chain_tool import SQLCustomTool
from src.services.csv_tool import CSVCustomTool
from langchain_community.chat_message_histories.upstash_redis import UpstashRedisChatMessageHistory
from langchain.tools import BaseTool, StructuredTool, tool
from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from pypdf import PdfReader
import faiss
from langchain_community.document_loaders import PyPDFLoader
import tiktoken
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from sqlalchemy.orm import Session


class RagService:
    def __init__(self, db: Session):
        self.user_dao = UserDAO(db)

    async def rag_response(self, user_query, user_id,file_name, session_id):
        load_dotenv()
        api_key=os.getenv("OPENAI_API_KEY")
        
        user_query = user_query + "dont tell me is there anything else you would like to know. Give me the final answer"

        llm = ChatOpenAI(
            openai_api_key=api_key,
            model_name='gpt-3.5-turbo',
            temperature=0
        )

        loader = PyPDFLoader(f"uploads/{file_name}")

        pages = loader.load_and_split()

        tokenizer = tiktoken.get_encoding('cl100k_base')

        embed = OpenAIEmbeddings(
            model='text-embedding-ada-002',
            openai_api_key=api_key
        )

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=400,
            chunk_overlap=20,
            length_function=tiktoken_len,
            separators=["\n\n", "\n", " ", ""]
        )
        data = text_splitter.split_documents(pages)
        db = FAISS.from_documents(data, self.embed)
        # llm = ChatOpenAI(
        #     openai_api_key="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",
        #     model_name='gpt-3.5-turbo',
        #     temperature=0.0
        # )
        retriever = db.as_retriever()
        
        db.save_local("faiss_index")

        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever
        )

        def tiktoken_len(text):
            tokens = tokenizer.encode(
                text,
                disallowed_special=()
            )
            return len(tokens)





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

        arxiv_tool = load_tools(["arxiv"])

        tools.extend(arxiv_tool)


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
        return output
       
