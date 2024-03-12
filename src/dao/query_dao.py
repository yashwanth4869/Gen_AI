from sqlalchemy.orm import Session
from src.models.qa_records import QARecords
from src.mapper.query_mapper import map_query
from fastapi import Response
from sqlalchemy import func

class QueryDAO:
    def __init__(self, db: Session):
        self.db = db        

    async def fetch_query(self, request):
        data = request.json()
        return data.get('user',None)
    
    async def add_record_to_db(self, user_id, query):
        record = map_query(user_id, query)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        
    async def update_status(self, task_id, status):
        record = self.db.query(QARecords).filter(QARecords.Id == task_id).fisrt()
        record.Status = status
        record.UpdatedAt = func.now()

    async def update_answer_field(self, task_id, generated_response):
        record = self.db.query(QARecords).filter(QARecords.Id == task_id).fisrt()
        record.Answer = generated_response
        record.UpdatedAt = func.now()

    
    

