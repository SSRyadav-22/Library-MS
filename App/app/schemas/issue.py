from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class IssueCreate(BaseModel):
    user_id: int
    book_id: int

class IssueOut(BaseModel):
    id: int
    user_id: int
    book_id: int
    issue_date: datetime
    due_date: datetime
    return_date: Optional[datetime]
    fine_amount: int
    status: str

    class Config:
        from_attributes = True

class ReturnOut(BaseModel):
    message: str
    fine_amount: int
    overdue_days: int
    return_date: datetime

class WaitlistCreate(BaseModel):
    book_id: int

class WaitlistOut(BaseModel):
    id: int
    user_id: int
    book_id: int
    position: int
    created_at: datetime

    class Config:
        from_attributes = True

class BookRequestCreate(BaseModel):
    title: str
    author: str
    isbn: Optional[str] = None
    remarks: Optional[str] = None

class BookRequestOut(BaseModel):
    id: int
    user_id: int
    title: str
    author: str
    isbn: Optional[str]
    remarks: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True