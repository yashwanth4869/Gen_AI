from sqlalchemy.orm import Session
from src.models.qa_records import QARecords
from fastapi import Response
from sqlalchemy import func
from fastapi.responses import JSONResponse
import json
import uuid
class UserDAO:
    def __init__(self, db:Session):
        self.db = db

    async def fetch_previous_chat(self, request):

        response_dictionary = {}
        session_id = await self.fetch_session_id(request)
        if not session_id:
            session_id = str(uuid.uuid4())
            response_dictionary['session_id'] = session_id
            response_dictionary['previous_chat'] = []
            return json.dumps(response_dictionary)

        previous_chat_questions = self.db.query(QARecords.Question).filter(QARecords.SessionId == session_id).all()
        previous_chat_answers = self.db.query(QARecords.Answer).filter(QARecords.SessionId == session_id).all()
        previous_chat = []
        for i in range(len(previous_chat_questions)):
            temp_dict = {}
            temp_dict['question'] = str(previous_chat_questions[i])
            temp_dict['answer'] = str(previous_chat_answers[i])
            previous_chat.append(temp_dict)
        response_dictionary['session_id'] = session_id
        response_dictionary['previous_chat'] = previous_chat

        return JSONResponse(content = response_dictionary)
    
    async def fetch_session_id(self, request):
        data = await request.json()
        return data.get('session_id', None)