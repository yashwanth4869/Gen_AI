from fastapi import APIRouter, Depends, HTTPException, Request,FastAPI
from fastapi.responses import Response
from sqlalchemy.orm import Session
from src.controllers.query_controller import QueryController
from src.config.database_initializer import get_db
from fastapi.responses import JSONResponse
from src.services.sql_services.sql_query_service import SQLQueryService
from src.services.sql_services.sql_query_service2 import SQLQueryService2
from src.services.sql_services.sql_chain import SQLService


router = APIRouter()

@router.post('/sql-query/{db_id}/{user_id}/{session_id}')
async def generate_sql_query_response(request : Request,db_id, user_id, session_id, db : Session = Depends(get_db)):
    return await SQLService(session_id).get_query_response(request)
    if(db_id=='1'):
        return await SQLQueryService(db).generate_sql_query_response(request, user_id, session_id)
    else:
        return await SQLQueryService2(db).generate_sql_query_response(request, user_id, session_id)
