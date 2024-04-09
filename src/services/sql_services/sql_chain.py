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

from langchain import FewShotPromptTemplate
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder,FewShotChatMessagePromptTemplate,PromptTemplate


class SQLService:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.db = SQLDatabase.from_uri('mysql+pymysql://root:123@localhost:3306/osione_dev')
        # print(self.db.table_info)
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
        # print(self.few_shot_prompt.format(input1="How many products are there?"))


        self.final_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a MySQL expert. Given an input question, create a syntactically correct MySQL query to run. Unless otherwise specificed.\n\nHere is the relevant table info: {table_info}\n\nBelow are a number of examples of questions and their corresponding SQL queries."),
                self.few_shot_prompt,
                ("human", "{input}"),
            ]
        )
    


        # self.example_template= """
        # User : {query}
        # AI: {result}
        # """

        # self.example_prompt=PromptTemplate(
        #     input_variables=["query","result", "top_k", "table_info"],
        #     template=self.example_template
        # )

        # self.prefix = """ You are a MySQL expert. Given an input question, create a syntactically correct MySQL query to run. Unless otherwise specificed.\n\nBelow are a number of examples of questions and their corresponding SQL queries."""

        # self.suffix = """
        # User : {query}
        # AI: """


        # self.few_shot_prompt_template=FewShotPromptTemplate(
        #     examples=self.examples,
        #     example_prompt=self.example_prompt,
        #     prefix=self.prefix,
        #     suffix=self.suffix,
        #     input_variables=['query']
        # )

        # print(few_shot_prompt_template.format(query=user_question))



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

    def get_property_information(self, user_question: str):
        
        # examples= [
        #     {
        #         "query" : "",
        #         "result" : ""
        #     }
        # ]

        # example_template= """
        # User : {query}
        # AI: {result}
        # """

        # example_prompt=PromptTemplate(
        #     input_variables=["query","result"],
        #     template=example_template
        # )

        # prefix = """ You are a MySQL expert. Given an input question, create a syntactically correct MySQL query to run. Unless otherwise specificed.\n\nBelow are a number of examples of questions and their corresponding SQL queries."""

        # suffix = """
        # User : {query}
        # AI: """


        # few_shot_prompt_template=FewShotPromptTemplate(
        #     examples=examples,
        #     example_prompt=example_prompt,
        #     prefix=prefix,
        #     suffix=suffix,
        #     input_variables=['query']
        # )

        # print(self.few_shot_prompt_template.format(query=user_question))

        print(self.final_prompt.format(input=user_question,table_info="some table info"))
        chain = (
            RunnablePassthrough.assign(query= self.generate_query | self.remove_sql_identifier).assign(
                result=itemgetter("query") | self.execute_query
            ) | self.rephrase_answer
        )
        output = chain.invoke({"question": user_question})
        return output

