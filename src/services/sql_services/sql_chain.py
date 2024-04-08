from langchain_community.utilities.sql_database import SQLDatabase
from dotenv import load_dotenv
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
import os

class SQLService:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.db = SQLDatabase.from_uri('mysql+pymysql://root:MANOsince%402003@localhost:3306/realestate_data')
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        self.generate_query = create_sql_query_chain(self.llm, self.db)
        self.execute_query = QuerySQLDataBaseTool(db=self.db)
        self.answer_prompt = PromptTemplate.from_template("""
            Given the following user question, corresponding SQL query, SQL result, answer the user question and rephrase the answer according to the user question.
            Question: {question},
            SQL Query: {query},
            SQL Result: {result}
            Answer: 
        """)
        self.rephrase_answer = self.answer_prompt | self.llm | StrOutputParser()

    def remove_sql_identifier(self,query:str):
        query = query.strip()
        if query.lower().startswith('```sql'):
            newline_index = query.find('\n') + 1
            last_newline_index = query.rfind('\n')+1
            return query[newline_index:last_newline_index]
        else:
            return query

    def get_property_information(self, user_question: str):
        chain = (
            RunnablePassthrough.assign(query= self.generate_query | self.remove_sql_identifier).assign(
                result=itemgetter("query") | self.execute_query
            ) | self.rephrase_answer
        )
        output = chain.invoke({"question": user_question})
        return output

