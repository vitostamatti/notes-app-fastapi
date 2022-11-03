from typing import List

from fastapi import Depends, HTTPException,APIRouter
from sqlalchemy.orm import Session

from sql import crud, models, schemas
from sql.database import SessionMaker, engine
from dependencies import get_db

router = APIRouter()


@router.post("/", response_model=schemas.NotesGroupRead)
def create_user(notes_group: schemas.NotesGroupCreate, db: Session = Depends(get_db)):
    db_group = crud.get_notes_group_by_name(db, name = notes_group.name)
    if db_group:
        raise HTTPException(status_code=400, detail="Group name already exists")
    return crud.create_notes_group(db=db, notes_group=notes_group)


@router.get("/", response_model=List[schemas.NotesGroupRead])
def get_notes_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    groups = crud.get_notes_groups(db, skip=skip, limit=limit)
    return groups


@router.get("/{group_id}", response_model=schemas.NotesGroupRead)
def get_notes_group(group_id: int, db: Session = Depends(get_db)):
    db_group = crud.get_notes_group(db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Notes Group not found")
    return db_group


@router.put("/{group_id}", response_model=schemas.NotesGroupRead)
def update_notes_group(group_id: int, notes_group: schemas.NotesGroupUpdate, db: Session = Depends(get_db)):
    db_notes_group = crud.get_notes_group(db=db, group_id=group_id)

    if not db_notes_group:
        raise HTTPException(status_code=404, detail=f"Notes group with id {group_id} not found")
    
    return crud.update_notes_group(db, db_notes_group, notes_group)
