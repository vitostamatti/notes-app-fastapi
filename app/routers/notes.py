from typing import List

from fastapi import Depends, HTTPException,APIRouter
from sqlalchemy.orm import Session

from sql import crud, models, schemas
from sql.database import SessionMaker, engine

from dependencies import get_db

router = APIRouter()

@router.post("/", response_model=schemas.NoteRead)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    db_note = crud.get_note_by_name(db, name = note.name)
    if db_note:
        raise HTTPException(status_code=400, detail="Note name already exists")
    return crud.create_note(db=db, note=note)


@router.get("/", response_model=List[schemas.NoteRead])
def read_notes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    notes = crud.get_notes(db, skip=skip, limit=limit)
    return notes


@router.put("/{note_id}", response_model=schemas.NoteRead)
def update_note(note_id: int, note: schemas.NoteUpdate, db: Session = Depends(get_db)):
    db_note = crud.get_note(db=db, note_id=note_id)
    
    if not db_note:
        raise HTTPException(status_code=404, detail=f"Note with id {note_id} not found")
    
    return crud.update_note(db, db_note, note)


@router.delete("/{note_id}", response_model=schemas.NoteRead)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    db_note = crud.get_note(db=db, note_id=note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail=f"Note with id {note_id} not found")
    
    return crud.delete_note(db, note_id)
    
    
