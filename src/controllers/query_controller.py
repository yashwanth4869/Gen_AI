from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.services.query_service import QueryService

class QueryController:
    def __init__(self, db : Session):
        self.query_service = QueryService(db)

    async def get_response(self, user_id, request):
        return await self.query_service.get_response(user_id, request)
    
    async def fetch_previous_chat(self, user_id):
        return await self.query_service.fetch_previous_chat(user_id)
