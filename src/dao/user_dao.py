from sqlalchemy.orm import Session
from src.models.qa_records import QARecords
from fastapi import Response
from sqlalchemy import func
from fastapi.responses import JSONResponse

class UserDAO:
    def __init__(self, db:Session):
        self.db = db

    async def fetch_previous_chat(self, user_id):
        previous_chat_questions = self.db.query(QARecords.Question).filter(QARecords.UserId == user_id).all()
        previous_chat_answers = self.db.query(QARecords.Answer).filter(QARecords.UserId == user_id).all()
        previous_chat = []
        for i in range(len(previous_chat_questions)):
            temp_dict = {}
            temp_dict['question'] = str(previous_chat_questions[i])
            temp_dict['answer'] = str(previous_chat_answers[i])
            previous_chat.append(temp_dict)

        return previous_chat