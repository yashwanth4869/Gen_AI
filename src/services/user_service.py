from sqlalchemy.orm import Session
from src.dao.user_dao import UserDAO
from fastapi import HTTPException, Response
from fastapi.responses import JSONResponse

class UserService:
    def __init__(self, db: Session):
        self.user_dao = UserDAO(db)

    async def fetch_previous_chat(self, request):
        return await self.user_dao.fetch_previous_chat(request)