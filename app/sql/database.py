# sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database settings

DATABASE_NAME = "database.db"
DATABASE_URL = f"sqlite:///{DATABASE_NAME}"

DATABASE_USER = ""
DATABASE_PASSWORD = ""
# DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@postgresserver/{DATABASE_NAME}"


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionMaker = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

Base = declarative_base()