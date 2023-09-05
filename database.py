import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
BASE_DIR=os.path.dirname(os.path.realpath(__file__))
connect="sqlite:///"+os.path.join(BASE_DIR,"school-app.db")
engine = create_engine(connect)
SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)
Base = declarative_base()