from sqlalchemy import (
    Boolean, Column, ForeignKey, Integer, String,
    DateTime
    )
from sqlalchemy.orm import relationship

from .database import Base


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    content = Column(String)
    notes_group_id = Column(Integer, ForeignKey("notes_groups.id"))
    
    notes_group = relationship("NotesGroup", back_populates="notes")
    

class NotesGroup(Base):
    __tablename__ = "notes_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    
    notes = relationship("Note", back_populates="notes_group")   