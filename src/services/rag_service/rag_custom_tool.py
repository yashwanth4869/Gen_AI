
from langchain.tools import BaseTool,StructuredTool, tool
from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from pypdf import PdfReader
import faiss
from langchain_community.document_loaders import PyPDFLoader
import tiktoken
import os
from dotenv import load_dotenv
 
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
 
 

class RagCustomTool(BaseTool):
    name ='RAG Custom Tool'
    description = 'Use this tool for any queries related to TS Epass of Manohar`'

    def __init__(self):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        self.loader = PyPDFLoader("uploads/Acknowledgment_Tsepass.pdf")
        self.pages = self.loader.load_and_split()
        self.tokenizer = tiktoken.get_encoding('cl100k_base')
        self.embed = OpenAIEmbeddings(
            model='text-embedding-ada-002',
            openai_api_key=api_key
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=400,
            chunk_overlap=20,
            length_function=self._tiktoken_len,
            separators=["\n\n", "\n", " ", ""]
        )
        self.data = self.text_splitter.split_documents(self.pages)
        self.db = FAISS.from_documents(self.data, self.embed)
        self.llm = ChatOpenAI(
            model_name='gpt-3.5-turbo',
            temperature=0.0
        )
        self.retriever = self.db.as_retriever()
        self.qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever
        )

    def _tiktoken_len(self, text):
        tokens = self.tokenizer.encode(
            text,
            disallowed_special=()
        )
        return len(tokens)
 
    def _run(self, user_query: str):
        output = self.qa.run(user_query)
        return output