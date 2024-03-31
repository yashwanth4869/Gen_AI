from fastapi import APIRouter, Depends, HTTPException, Request,FastAPI
from fastapi.responses import Response
from sqlalchemy.orm import Session
from src.controllers.query_controller import QueryController
from src.config.database_initializer import get_db
from fastapi.responses import JSONResponse
from src.services.sql_services.sql_query_service import SQLQueryService


router = APIRouter()

@router.post('/sql-query/{user_id}/{session_id}')
async def generate_sql_query_response(request : Request, user_id, session_id, db : Session = Depends(get_db)):
    return await SQLQueryService(db).generate_sql_query_response(request, user_id, session_id)

