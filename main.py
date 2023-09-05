import model
from database import engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from authentication.auth import auth_router
model.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)