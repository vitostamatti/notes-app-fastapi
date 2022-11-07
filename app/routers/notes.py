from typing import List, Any

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from app.routers import dependencies as deps
from app.crud import crud
from app.models import models
from app.schemas import schemas


router = APIRouter()


@router.get("/", response_model=List[schemas.NoteRead])
def get_notes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
    ):

    notes = crud.get_notes_by_author(
        db=db, 
        author_id=current_user.id,
        skip=skip, limit=limit
        )
    return notes


@router.get("/all", response_model=List[schemas.NoteRead])
def get_notes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
    ):
    notes = crud.get_notes(db=db, skip=skip, limit=limit)
    return notes


@router.post("/", response_model=schemas.NoteRead)
def create_note(
    note: schemas.NoteCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    db_note = crud.get_note_by_name(db, name=note.name)
    if db_note and db_note.author_id == current_user.id:
        raise HTTPException(status_code=400, detail="Note name already exists")

    return crud.create_note(db=db, author_id=current_user.id, note=note)


@router.get("/{note_id}", response_model=schemas.NoteRead)
def get_note_by_id(
    note_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific note by id.
    """

    note = crud.get_note(db, note_id=note_id)
    print(note)

    if (note.author_id != current_user.id) and not (current_user.is_superuser):
        raise HTTPException(
            status_code=404,
            detail="You're not allowed to access this note.",
        )

    if not note:
        raise HTTPException(
            status_code=404,
            detail="The note with this id does not exist in the system.",
        )

    return note


@router.put("/{note_id}", response_model=schemas.NoteRead)
def update_note(
    note_id: int,
    note: schemas.NoteUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    db_note = crud.get_note(db=db, note_id=note_id)

    if not db_note:
        raise HTTPException(status_code=404, detail=f"Note with id {note_id} not found")

    if db_note.author_id != current_user.id:
        raise HTTPException(status_code=402, detail="User not authorized")

    return crud.update_note(db, db_note, note)


@router.delete("/{note_id}", response_model=schemas.NoteRead)
def delete_note(
    note_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    db_note = crud.get_note(db=db, note_id=note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail=f"Note with id {note_id} not found")

    if db_note.author_id != current_user.id:
        raise HTTPException(status_code=402, detail="User not authorized")

    return crud.delete_note(db, note_id)
