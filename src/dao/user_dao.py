from sqlalchemy.orm import Session
from src.models.qa_records import QARecords
from src.models.users import Users
from src.mapper.query_mapper import map_query
from fastapi import Response
from sqlalchemy import func
from fastapi.responses import JSONResponse

class UserDAO:
    def __init__(self, db:Session):
        self.db = db

    async def fetch_user_memory(self,user_id):
        user_model = self.db.query(Users.UserModel).filter(Users.Id == user_id).first()
        return user_model