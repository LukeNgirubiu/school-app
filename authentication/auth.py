from fastapi import APIRouter,Depends,status
from datetime import timedelta
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from .form_model import SchoolData,User,Settings,Login
import model
from sqlalchemy import or_
from sessions import get_db
auth_router=APIRouter()
post=auth_router.post
get=auth_router.get
bcrypt_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
def get_password_hash(Password):
   return bcrypt_context.hash(Password)
@AuthJWT.load_config
def get_config():
    return Settings()

@post("/register/school",status_code=201)
async def post_school(school:SchoolData,db:Session=Depends(get_db)):#
    try:
        school_exist=db.query(model.SchoolData).filter(or_(model.SchoolData.Name ==school.name,
                                                            model.SchoolData.Phone ==school.phone,
                                                            model.SchoolData.Address ==school.address
                                                            )).first()
        print("Address here ",school.address)
        #print(school_exist.Address)
        if school_exist is not None:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content={"status":"failed","message":"Details provided already exist"})
        db_school=model.SchoolData()
        print(f"DB school {db_school.Address}")
        db_school.Address=school.address
        db_school.Level=school.level
        db_school.Phone=school.phone
        db_school.Location=school.location
        db_school.Name=school.name
        db.add(db_school)
        db.commit()
        return {"status":'success',"id":db_school.Id}
    except Exception as ex:
        print("Error ",str(ex))
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"status":"failed","message":str(ex)})


@post("/register/staff/{Id}",status_code=201)
async def post_staff(Id:int,staff:User,db:Session=Depends(get_db)):#
    try:
        school=db.query(model.SchoolData).filter(model.SchoolData.Id==Id).first()
        user=db.query(model.User).filter(model.User.Email==staff.email).first()
        if user is not None:
            return JSONResponse(status_code=400,
                                content={"status":"failed","message":"Details provided already exist"})
        if school is not None:
            db_user=model.User()
            db_user.Email=staff.email
            db_user.Role=staff.role
            db_user.Name=staff.name
            db_user.SchoolId=Id
            db_user.Password=get_password_hash(staff.password)
            db.add(db_user)
            db.commit()
            return {"status":"success"}
        else:
            return JSONResponse(status_code=401,
                                content={"status":"failed","message":"School doesn't exist"})
    except Exception as ex:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"status":"failed","message":str(ex)})
@get("/register/test",status_code=201)
async def get_staff(db:Session=Depends(get_db)):
    return {
        "school":db.query(model.SchoolData).all(),
        "staffs":db.query(model.User).all(),
    } 
@post("/staff/login",status_code=201)
async def login_staff(login:Login,db:Session=Depends(get_db),Authorize:AuthJWT=Depends()):
    try:
        user=db.query(model.User).filter(model.User.Email==login.email).first()
        if user is None:
            return JSONResponse(status_code=404,
                                    content={"status":"failed","message":"User with this email doesn't exist"})
        if user is not None:
            validate=bcrypt_context.verify(login.password,user.Password)
            if validate==True:
                school=db.query(model.SchoolData).filter(model.SchoolData.Id==user.SchoolId).first()
                claims={"role":school.Level,"InstituitionId":school.Id}
                expires = timedelta(hours=10)
                token=Authorize.create_access_token(subject=user.Id,algorithm="HS256",expires_time=expires,user_claims=claims)
                refresh=Authorize.create_refresh_token(subject=user.Id,algorithm="HS256",expires_time=expires,user_claims=claims)
                return {
                    "token":token,
                    "refresh_token":refresh
                }
            else:
                return JSONResponse(status_code=401,
                                content={"status":"failed","message":"Invalid password"})
    except Exception as ex:
        return JSONResponse(status_code=500,
                                content={"status":"failed","message":str(ex)})



