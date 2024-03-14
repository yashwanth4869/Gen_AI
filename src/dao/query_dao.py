from sqlalchemy.orm import Session
from src.models.qa_records import QARecords
from src.mapper.query_mapper import map_query
from fastapi import Response
from sqlalchemy import func
from fastapi.responses import JSONResponse

class QueryDAO:
    def __init__(self, db: Session):
        self.db = db        

    
    
    async def add_record_to_db(self, user_id, query):
        record = map_query(user_id, query)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record.Id
        
    async def update_status(self, task_id, status):
        record = self.db.query(QARecords).filter(QARecords.Id == task_id).first()
        record.Status = status
        record.UpdatedAt = func.now()
        self.db.commit()

    async def update_answer_field(self, task_id, generated_response):
        record = self.db.query(QARecords).filter(QARecords.Id == task_id).first()
        record.Answer = generated_response
        record.UpdatedAt = func.now()
        self.db.commit()

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


    
    

