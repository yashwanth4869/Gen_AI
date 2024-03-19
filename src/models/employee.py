from sqlalchemy import  Column, Integer, String, Text, TIMESTAMP, ForeignKey, Enum, Date, Float
from src.config.database import base
from sqlalchemy.sql import func

class Dept(base):
    __tablename__ = 'dept'
    DeptNo = Column(Integer,primary_key=True)
    DName = Column(Text)
    Loc = Column(Text)

class Emp(base):
    __tablename__ = 'emp'
    EmpNo = Column(Integer, primary_key=True)
    Ename = Column(Text)
    Job = Column(Text)
    MGR = Column(Integer)
    HireDate = Column(Date)
    Sal = Column(Float)
    Comm = Column(Float)
    DeptNo = Column(Integer, ForeignKey(Dept.DeptNo))




