from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.services.user_service import UserService

class UserController:
    def __init__(self, db : Session):
        self.user_service = UserService(db)
    
    async def fetch_session_chat(self, request):
        return await self.user_service.fetch_session_chat(request)
    
    async def fetch_user_conversations(self,request):
        return await self.user_service.fetch_user_conversations(request)