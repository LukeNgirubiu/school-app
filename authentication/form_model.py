from pydantic import BaseModel
class User(BaseModel):
    name:str
    role:str
    email:str
    password:str
class SchoolData(BaseModel):
    address:str
    location:str
    phone:str
    level:str
    name:str
class Settings(BaseModel):
    authjwt_secret_key:str='lukeson'
class Login(BaseModel):
    email:str
    password:str
