from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.controllers.query_controller import QueryController
from src.config.database_initializer import get_db

router = APIRouter()