from typing import List

from fastapi import Depends, HTTPException,APIRouter
from sqlalchemy.orm import Session

from app.crud import crud
from app.models import models
from app.schemas import schemas
from app.routers import dependencies as deps

router = APIRouter()


@router.post("/", response_model=schemas.NotesGroupRead)
def create_notes_group(
    notes_group: schemas.NotesGroupCreate, 
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
    ):
    db_group = crud.get_notes_group_by_name(db, name = notes_group.name)
    
    if db_group and db_group.author_id==current_user.id:
        raise HTTPException(status_code=400, detail="Group name already exists")

    return crud.create_notes_group(db=db, notes_group=notes_group)


@router.get("/", response_model=List[schemas.NotesGroupRead])
def get_notes_groups(
        skip: int = 0, 
        limit: int = 100, 
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
    ):
    groups = crud.get_notes_groups_by_author(
        db, 
        author_id=current_user.id, 
        skip=skip, limit=limit
    )
    return groups


@router.get("/{group_id}", response_model=schemas.NotesGroupRead)
def get_notes_group(
    group_id: int, 
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
    ):
    db_group = crud.get_notes_group(db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Notes Group not found")

    if db_group.author_id != current_user.id:
        raise HTTPException(status_code=402, detail=f"User not authorized")

    return db_group


@router.put("/{group_id}", response_model=schemas.NotesGroupRead)
def update_notes_group(
    group_id: int, 
    notes_group: schemas.NotesGroupUpdate, 
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
    ):
    db_group = crud.get_notes_group(db=db, group_id=group_id)

    if not db_group:
        raise HTTPException(status_code=404, detail=f"Notes group with id {group_id} not found")

    if db_group.author_id != current_user.id:
        raise HTTPException(status_code=402, detail=f"User not authorized")

    return crud.update_notes_group(db, db_group, notes_group)
