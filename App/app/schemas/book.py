from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BookCreate(BaseModel):
    title: str
    author: str
    isbn: Optional[str] = None
    total_copies: int

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    total_copies: Optional[int] = None
    is_active: Optional[bool] = None

class BookOut(BaseModel):
    id: int
    title: str
    author: str
    isbn: Optional[str]
    total_copies: int
    available_copies: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class BookAvailability(BaseModel):
    id: int
    title: str
    author: str
    isbn: Optional[str]
    available_copies: int
    total_copies: int
    expected_return_date: Optional[datetime] = None
    waitlist_count: int = 0

    class Config:
        from_attributes = True