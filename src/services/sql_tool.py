from langchain.tools import BaseTool,StructuredTool, tool
from langchain.agents.agent_types import AgentType
from langchain.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from src.config.database import engine
from langchain_community.agent_toolkits import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain import OpenAI
from dotenv import load_dotenv
import os



class SQLCustomTool(BaseTool):
    name = "SQL querying tool"
    description = '''
                    **I want sql query to run everytime whenever data related to properties or data related to houses or data related to real estate is needed.
                    **Use this tool when you need to answer the questions related to RealEstate Data or RelaEstate Database. The user can also query using words like "house, property, city, state, size, other terminologies related to houses or properties, etc".  "Expects a question from the user and queries that question and return the answer according to the data present" "To use this tool you must provide the direct question from user
                    **The table consists of fields- 
                    *id, 
                    *status (for_sale or sold out), 
                    *Bed (represents numbers of bedrooms in house or property),
                    *Bath (reprsents number of bathrooms in the property),
                    *AcreLot,
                    *City,
                    *State,
                    *ZipCode,
                    *HouseSize (represnts the size of the house),
                    *Price (represnts cost of the house/property) 
                    
                    **There is also an employee table named as emp which is related with department table which is named as dept.
                    **User can query words like boss, id, manager etc. The fields in the emp table are:
                    *empno depicts employee id
                    *ename depicts employee name
                    *deptno is department
                    *mgr is the id of the manager of the employee or their direct boss
                    sal is their salary
                    
                    **The dept table is related with emp table and has the following columns:
                    *deptno is id of the department
                    *dname is the name of the department
                    *loc is the location(city)
                    "'''

    def _run(self,query:str):
        load_dotenv()
        api_key=os.getenv("OPENAI_API_KEY")

        llm = OpenAI(
            openai_api_key=api_key,
            temperature=0
        )
        db = SQLDatabase(engine)
        agent = create_sql_agent(   
            llm=llm,
            toolkit=SQLDatabaseToolkit(db=db, llm=llm),
            verbose=True,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            top_k=1000
            )
        return agent.run(query)
    
    def _arun(self,query:str):
        raise NotImplementedError("This tool does not support async :")


# @tool
# ""
# def sql_custom_agent(query:str):

#     load_dotenv()
#     api_key=os.getenv("OPENAI_API_KEY")

#     llm = OpenAI(
#         openai_api_key=api_key,
#         temperature=0
#     )
#     db = SQLDatabase(engine)
#     agent = create_sql_agent(   
#         llm=llm,
#         toolkit=SQLDatabaseToolkit(db=db, llm=llm),
#         verbose=True,
#         agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#         top_k=1000
#         )
#     return agent.run(query)