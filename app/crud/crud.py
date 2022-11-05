
from sqlalchemy.orm import Session
from typing import Union, List
from app.models import models
from app.schemas import schemas
from typing import Optional

from app.core.security import get_password_hash, verify_password

### Users
def get_user(db: Session, user_id: int) -> Union[models.User,None]:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> Union[models.User,None]:
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Union[models.User,None]:
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(
        username=user.username,
        hashed_password=get_password_hash(user.password),
        email= user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, db_user: models.User, user: schemas.UserUpdate) -> models.User:
    user_data = user.dict(exclude_unset=True)
    if user_data["password"]:
        hashed_password = get_password_hash(user_data["password"])
        del user_data["password"]
        user_data["hashed_password"] = hashed_password

    for key, value in user_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id:int) -> models.User:
    db_user = get_note(db, user_id)
    db.delete(db_user)
    db.commit()
    return db_user


def authenticate_user(db: Session, username: str, password: str) -> Optional[models.User]:
    user = get_user_by_username(db, username=username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def user_is_active(user: models.User) -> bool:
    return user.is_active

def user_is_superuser(user: models.User) -> bool:
    return user.is_superuser


### Notes
def get_note(db: Session, note_id: int):
    return db.query(models.Note).filter(models.Note.id == note_id).first()


def get_note_by_name(db: Session, name: str):
    return db.query(models.Note).filter(models.Note.name == name).first()


def get_notes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Note).offset(skip).limit(limit).all()


def get_notes_by_author(db: Session, author_id:int, skip: int = 0, limit: int = 100):
    return db.query(models.Note).filter(
        models.Note.author_id == author_id
        ).offset(skip).limit(limit).all()


def create_note(db: Session, author_id:int, note: schemas.NoteCreate):
    if not note.notes_group_id:
        default_notes_group = db.query(models.NotesGroup).filter(
            models.NotesGroup.name == 'Default'
            ).first()
        notes_group_id = default_notes_group.id
    else:
        notes_group_id = note.notes_group_id
    
    db_note = models.Note(
        name=note.name, 
        content=note.content, 
        notes_group_id=notes_group_id,
        author_id=author_id
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

def get_notes_groups_by_author(db: Session, author_id:int, skip: int = 0, limit: int = 100) -> Union[List[models.NotesGroup],List[None]]:
    return db.query(models.NotesGroup).filter(
        models.NotesGroup.author_id == author_id
        ).offset(skip).limit(limit).all()


def create_notes_group(db: Session, author_id: int, notes_group: schemas.NotesGroupCreate):
    db_notes_group = models.NotesGroup(name=notes_group.name, author_id=author_id)
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