# from fastapi import FastAPI, APIRouter, HTTPException, Depends, status,Header, Query,Request
# from fastapi.middleware.cors import CORSMiddleware
# from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from pypdf import PdfReader
import faiss
from langchain_community.document_loaders import PyPDFLoader
import tiktoken
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv
from langchain import OpenAI
# import pathlib
# import aiofiles
import time
from src.services.rag_services.token_len import tiktoken_len
# from fastapi import File, UploadFile



async def rag_db(filename, session_id):
    # db_filename = f"FAISS_DB/static1+faiss_index"
    # file_path = f'uploads/{filename}'
    index_path = f'FAISS_DB/{session_id}'

    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    llm = ChatOpenAI(
        openai_api_key=api_key,
        model_name='gpt-3.5-turbo',
        temperature=0
    )
    embed = OpenAIEmbeddings(
            model='text-embedding-ada-002',
            openai_api_key=api_key
        )
    
    db = FAISS.load_local(index_path,embed, allow_dangerous_deserialization=True)
    retriever = db.as_retriever()

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever
    )
    
    return qa


async def add_file_to_vector_store(file_path, session_id):
    index_path = f'FAISS_DB/{session_id}'
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    llm = ChatOpenAI(
        openai_api_key=api_key,
        model_name='gpt-3.5-turbo',
        temperature=0
    )
    # time.sleep(2)
    embed = OpenAIEmbeddings(
            model='text-embedding-ada-002',
            openai_api_key=api_key
        )
    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()
    tokenizer = tiktoken.get_encoding('cl100k_base')
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=100,
        length_function = tiktoken_len,
        separators=["\n\n", "\n", " ", ""]
    )
    data = text_splitter.split_documents(pages)
    if not os.path.exists(index_path):
        db = FAISS.from_documents(data, embed)
        db.save_local(index_path)
    else:
        db = FAISS.load_local(index_path, embed, allow_dangerous_deserialization=True)
        db.add_documents(data)
        db.save_local(index_path)