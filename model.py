from sqlalchemy import Column,Integer,String,ForeignKey
from database import Base
class User(Base):
    __tablename__="Users"
    Id=Column(Integer,primary_key=True,index=True)
    Role=Column(String)
    Name=Column(String(100))
    Email=Column(String(50),unique=True)
    Password=Column(String(300))
    SchoolId=Column(Integer,ForeignKey('Institution.Id'))
class SchoolData(Base):
    __tablename__="Institution"
    Id=Column(Integer,primary_key=True,index=True)
    Name=Column(String(100))
    Address=Column(String(80))
    Location=Column(String(70))
    Phone=Column(String(20),unique=True)
    Level=Column(String(100))
 