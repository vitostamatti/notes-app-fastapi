from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sql import crud, models, schemas
from sql.database import SessionMaker, engine
from routers import notes

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(notes_groups.router, prefix="/notes_groups", tags=["notes_groups"])
app.include_router(notes.router, prefix="/notes", tags=["notes"])