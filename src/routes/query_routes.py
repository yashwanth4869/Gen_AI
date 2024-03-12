from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import Response
from sqlalchemy.orm import Session
from src.controllers.query_controller import QueryController
from src.config.database_initializer import get_db
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post('/query/{user_id}')
async def generate_answer(user_id, request : Request, db : Session = Depends(get_db)):
    return await QueryController(db).get_response(user_id, request)

@router.get('/query/{user_id}')
async def fetch_previous_chat(user_id, db : Session = Depends(get_db)):
    return await QueryController(db).fetch_previous_chat(user_id)