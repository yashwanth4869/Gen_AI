from langchain.tools import BaseTool,StructuredTool, tool
from typing import Any
 
 
 
class RagCustomTool(BaseTool):
    name ='RAG Custom Tool'
    description = 'Use this tool for any queries related to the uploaded document. *If there is a question like "what is the uploaded document about" then parse the uploaded document.'
    qa : Any
 
       
    def _run(self, user_query: str):
        # print(self.qa)
        output = self.qa.run(user_query)
        return output
 
    def _arun(self):
        raise NotImplementedError("This tool does not support async :")