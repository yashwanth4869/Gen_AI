from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from src.services.qnaService.chatService import QueryService
from src.utils.databaseInitializer import get_db

router = APIRouter()

@router.post('/query/{user_id}/{id}')
async def generate_response(request : Request,user_id:int,id, db : Session = Depends(get_db)):
    return await QueryService(db).generate_response(request,user_id,id)

@router.post('/query/{user_id}')
async def generate_response(request : Request,user_id:int, db : Session = Depends(get_db)):
    id=None
    return await QueryService(db).generate_response(request,user_id,id)

