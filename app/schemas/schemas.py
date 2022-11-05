from typing import List, Union, Optional

from pydantic import BaseModel

# Notes
class NoteBase(BaseModel):
    name:str
    content:Optional[str] = None


class NoteCreate(NoteBase):
    notes_group_id: Optional[int] = None

class NoteRead(NoteBase):
    id: int
    author_id: int
    notes_group_id: int

    class Config:
        orm_mode = True
        
class NoteUpdate(BaseModel):
    name:Optional[str] = None
    content:Optional[str]= None
    notes_group_id: Optional[int] = None


# Notes Groups
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


# Access Token
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None



# User
class UserBase(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    username: str
    email: str
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


# DB schemas
class UserRead(UserBase):
    id: int 
    notes: List[NoteRead] = []
    is_active: bool   
    class Config:
        orm_mode = True


# Additional properties stored in DB
class UserWrite(UserRead):
    hashed_password: str

