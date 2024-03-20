from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import Response
from sqlalchemy.orm import Session
from src.controllers.user_controller import UserController
from src.config.database_initializer import get_db
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get('/user/session')
async def fetch_previous_chat(request : Request, db : Session = Depends(get_db)):
    return await UserController(db).fetch_previous_chat(request)

@router.get('/user/conversations')
async def fetch_user_conversations(request : Request, db : Session = Depends(get_db)):
    return await UserController(db).fetch_user_conversations(request)