from sqlalchemy import  Column, Integer, String, Text, TIMESTAMP, ForeignKey, Enum
from src.config.database import base
from sqlalchemy.sql import func

class Users(base):
    __tablename__ = "users"
    Id = Column(Integer, primary_key=True)
    UserModel = Column(Text)