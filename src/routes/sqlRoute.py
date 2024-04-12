from fastapi import APIRouter, Depends, HTTPException, Request,FastAPI
from sqlalchemy.orm import Session
from src.utils.databaseInitializer import get_db
from src.services.sqlService.sqlChain import SQLService


router = APIRouter()

@router.post('/sql-query/{user_id}/{session_id}')
async def generate_sql_query_response(request : Request, user_id, session_id, db : Session = Depends(get_db)):
    return await SQLService(session_id, db).get_query_response(request, user_id, session_id)
