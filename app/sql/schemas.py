from typing import List, Union, Optional

from pydantic import BaseModel


class NoteBase(BaseModel):
    name:str
    content:str
    notes_group_id: Optional[int] = None


class NoteCreate(NoteBase):
    pass


class NoteRead(NoteBase):
    id: int

    class Config:
        orm_mode = True
        
        
class NoteUpdate(BaseModel):
    name: Optional[str] = None
    secret_name: Optional[str] = None
    age: Optional[int] = None



class NotesGroupBase(BaseModel):
    name:str


class NotesGroupCreate(NotesGroupBase):
    pass


class NotesGroupRead(NotesGroupBase):
    id: int
    notes: List[NoteRead] = []

    class Config:
        orm_mode = True
        
        
class NotesGroupUpdate(BaseModel):
    name: Optional[str] = None