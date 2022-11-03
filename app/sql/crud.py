
from sqlalchemy.orm import Session
from typing import Union, List
import models, schemas, database


def create_db_and_tables():
    models.Base.metadata.create_all(database.engine)


def get_note(db: Session, note_id: int):
    return db.query(models.Note).filter(models.Note.id == note_id).first()


def get_note_by_name(db: Session, name: str):
    return db.query(models.Note).filter(models.Note.name == name).first()


def get_notes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Note).offset(skip).limit(limit).all()


def create_note(db: Session, note: schemas.NoteCreate):
    db_note = models.Note(
        name=note.name, content=note.content, 
        notes_group_id=note.notes
        )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def update_note(db: Session, db_note:models.Note, note:schemas.NoteUpdate):
    
    note_data = note.dict(exclude_unset=True)
    
    for key, value in note_data.items():
        setattr(db_note, key, value)
        
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    
    return db_note

    
def delete_note(db: Session, note_id:int):
    db_note = get_note(db, note_id)
    db.delete(db_note)
    db.commit()
    return db_note


def get_notes_group(db: Session, group_id: int) -> Union[models.NotesGroup,None]:
    return db.query(models.NotesGroup).filter(models.NotesGroup.id == group_id).first()


def get_notes_group_by_name(db: Session, name: str) -> Union[models.NotesGroup,None]:
    return db.query(models.NotesGroup).filter(models.NotesGroup.name == name).first()


def get_notes_groups(db: Session, skip: int = 0, limit: int = 100) -> Union[List[models.NotesGroup],List[None]]:
    return db.query(models.NotesGroup).offset(skip).limit(limit).all()


def create_notes_group(db: Session, notes_group: schemas.NotesGroupCreate):
    db_notes_group = models.NotesGroup(name=notes_group.name)
    db.add(db_notes_group)
    db.commit()
    db.refresh(db_notes_group)
    return db_notes_group


def update_notes_group(db: Session, db_notes_group: models.NotesGroup, notes_group: schemas.NotesGroupUpdate):
    notes_group_data = notes_group.dict(exclude_unset=True)
    
    for key, value in notes_group_data.items():
        setattr(db_notes_group, key, value)
        
    db.add(db_notes_group)
    db.commit()
    db.refresh(db_notes_group)
    return db_notes_group
    
    
def delete_notes_group(db: Session, group_id:int):
    db_notes_group = get_notes_group(db, group_id)
    db.delete(db_notes_group)
    db.commit()
    return db_notes_group