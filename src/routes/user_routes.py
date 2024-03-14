from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import Response
from sqlalchemy.orm import Session
from src.controllers.user_controller import UserController
from src.config.database_initializer import get_db
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get('/queries/user/{user_id}')
async def fetch_previous_chat(user_id, db : Session = Depends(get_db)):
    return await UserController(db).fetch_previous_chat(user_id)