from sqlalchemy.orm import Session
from typing import Union, List
from app.models import models
from app.schemas import schemas
from typing import Optional
from fastapi.encoders import jsonable_encoder
from app.core.security import get_password_hash, verify_password

### Users
def get_users(
    db: Session, skip: int = 0, limit: int = 100
) -> List[Union[models.User, None]]:
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int) -> Union[models.User, None]:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> Union[models.User, None]:
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Union[models.User, None]:
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(
        username=user.username,
        hashed_password=get_password_hash(user.password),
        email=user.email,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(
    db: Session, db_user: models.User, user: schemas.UserUpdate
) -> models.User:
    user_data = user.dict(exclude_unset=True)
    if user_data.get("password", None):
        hashed_password = get_password_hash(user_data["password"])
        del user_data["password"]
        user_data["hashed_password"] = hashed_password

    db_user_data = jsonable_encoder(db_user)
    for field in db_user_data:
        if field in user_data:
            setattr(db_user, field, user_data[field])

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> models.User:
    db_user = get_user(db, user_id)
    db.delete(db_user)
    db.commit()
    return db_user


def authenticate_user(
    db: Session, username: str, password: str
) -> Optional[models.User]:
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


def get_note_by_name(db: Session, name: str) -> schemas.NoteRead:
    return db.query(models.Note).filter(models.Note.name == name).first()


def get_notes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Note).offset(skip).limit(limit).all()


def get_notes_by_author(db: Session, author_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Note)
        .filter(models.Note.author_id == author_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_note(db: Session, author_id: int, note: schemas.NoteCreate):
    db_note = models.Note(name=note.name, content=note.content, author_id=author_id)

    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    return db_note


def update_note(db: Session, db_note: models.Note, note: schemas.NoteUpdate):

    note_data = note.dict(exclude_unset=True)

    for key, value in note_data.items():
        setattr(db_note, key, value)

    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    return db_note


def delete_note(db: Session, note_id: int):
    db_note = get_note(db, note_id)
    db.delete(db_note)
    db.commit()
    return db_note
