from sqlalchemy.orm import Session
from src.dao.query_dao import QueryDAO
from fastapi import HTTPException, Response
from src.services.gen_ai_service import GenAiService
from fastapi.responses import JSONResponse

# class QueryService:
#     def __init__(self, db: Session):
#         self.query_dao = QueryDAO(db)
#         self.gen_ai = GenAiService()
    
#     async def get_response(self, user_id, request):
#         user_query = await self.fetch_query(request)
#         task_id = self.query_dao.add_record_to_db(user_id, user_query)
#         self.query_dao.update_status(task_id, 'Inprogress')

#         generated_response = self.gen_ai.generate_response(user_query)

#         self.query_dao.update_answer_field(task_id, generated_response)
#         self.query_dao.update_status(task_id, 'Completed')
#         return JSONResponse(content = generated_response)
    
#     async def fetch_query(self, request):
#         data = await request.json()
#         return data.get('user',None)

class QueryService:
    def __init__(self, db: Session):
        self.query_dao = QueryDAO(db)
        self.gen_ai = GenAiService()
    
    async def get_response(self, user_id, request):
        user_query = await self.fetch_query(request)
        task_id = await self.query_dao.add_record_to_db(user_id, user_query)
        await self.query_dao.update_status(task_id, 'Inprogress')

        generated_response = await self.gen_ai.generate_response(user_query)

        await self.query_dao.update_answer_field(task_id, generated_response)
        await self.query_dao.update_status(task_id, 'Completed')
        return JSONResponse(content=generated_response)
    
    async def fetch_previous_chat(self, user_id):
        return await self.query_dao.fetch_previous_chat(user_id)
    
    async def fetch_query(self, request):
        data = await request.json()
        return data.get('user', None)