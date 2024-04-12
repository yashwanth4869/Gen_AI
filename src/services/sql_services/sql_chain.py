from langchain_community.utilities.sql_database import SQLDatabase
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAI
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
import os
from langchain_community.chat_message_histories.upstash_redis import UpstashRedisChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder,FewShotChatMessagePromptTemplate,PromptTemplate
from sqlalchemy.orm import Session
from src.dao.query_dao import QueryDAO

class SQLService:
    def __init__(self, session_id, db : Session):
        self.query_dao = QueryDAO(db)
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.history = UpstashRedisChatMessageHistory(
            url = os.getenv("REDIS_URL"),
            token = os.getenv("REDIS_TOKEN"),
            session_id = session_id,
        )
        self.uri_key = os.getenv("SAMPLE_DB_URL")
        self.db = SQLDatabase.from_uri(self.uri_key)
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=self.api_key)

        self.examples= [
            {
                "input" : "Total recognized revenue for each project",
                "query" : "SELECT project, SUM(recognized_revenue) AS total_recognized_revenue FROM osi_rev_rec_tabx GROUP BY project;"
            },
            {
                "input" : "Average billable hours per employee",
                "query" : "SELECT employee, AVG(billable_hours) AS avg_billable_hours FROM osi_rev_rec_tabx GROUP BY employee;"
            },
            {
                "input" : "Total recognized revenue and cost by month",
                "query" : "SELECT yearmonth, SUM(recognized_revenue) AS total_recognized_revenue, SUM(recognized_cost) AS total_recognized_cost FROM osi_rev_rec_tabx GROUP BY yearmonth;"
            }
        ]


        self.example_prompt = ChatPromptTemplate.from_messages(
            [
                ("human", "{input}\nSQLQuery:"),
                ("ai", "{query}"),
            ]
        )
        self.few_shot_prompt = FewShotChatMessagePromptTemplate(
            example_prompt=self.example_prompt,
            examples=self.examples,
            input_variables=["input","top_k"],
        )

        self.final_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a MySQL expert. Given an input question, create a syntactically correct MySQL query to run. Unless otherwise specificed.\n\nHere is the relevant table info: {table_info}\n\nBelow are a number of examples of questions and their corresponding SQL queries."),
                self.few_shot_prompt,
                MessagesPlaceholder(variable_name="messages"),
                ("human", "{input}"),
            ]
        )

        self.generate_query = create_sql_query_chain(self.llm, self.db, self.final_prompt)
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
        print("query", query)
        if query.lower().startswith('```sql'):
            newline_index = query.find('\n') + 1
            last_newline_index = query.rfind('\n')+1
            return query[newline_index:last_newline_index]
        else:
            return query

    async def get_query_response(self, request, user_id, session_id):
        data = await request.json()
        user_query = data.get('user', None)
        
        chain = (
            RunnablePassthrough.assign(query= self.generate_query | self.remove_sql_identifier).assign(
                result=itemgetter("query") | self.execute_query
            ) | self.rephrase_answer
        )
        task_id = await self.query_dao.add_record_to_db(user_id, user_query,session_id, 'SQLService')
        await self.query_dao.update_status(task_id, 'Inprogress')
        output = chain.invoke({"question": user_query, "messages" : self.history.messages})
        await self.query_dao.update_answer_field(task_id, output)
        await self.query_dao.update_status(task_id, 'Completed')
        self.history.add_user_message(user_query)
        self.history.add_ai_message(output)
        return {'bot': output, 'session_id':session_id}

