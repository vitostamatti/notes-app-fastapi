from sqlalchemy import (
    Boolean, Column, 
    ForeignKey, Integer, String,
    DateTime
    )
from sqlalchemy.orm import relationship

from app.database.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    
    notes = relationship("Note", back_populates="author")


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    content = Column(String)
    author_id = Column(Integer, ForeignKey("users.id"))
    notes_group_id = Column(Integer, ForeignKey("notes_groups.id"))
    
    notes_group = relationship("NotesGroup", back_populates="notes")
    author = relationship("User", back_populates="notes")



class NotesGroup(Base):
    __tablename__ = "notes_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"))

    notes = relationship("Note", back_populates="notes_group")   



