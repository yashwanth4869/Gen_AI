from sqlalchemy.orm import Session
from src.dao.query_dao import QueryDAO
from fastapi import HTTPException

class QueryService:
    def __init__(self, db: Session):
        self.query_dao = QueryDAO(db)

    async def get_response(self, user_id, request):
        return await self.query_dao.get_response(user_id, request)