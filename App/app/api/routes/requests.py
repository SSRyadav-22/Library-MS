from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.issue import BookRequestCreate, BookRequestOut
from app.crud.issue import create_book_request, list_book_requests, get_book_request, update_book_request_status
from app.api.deps import get_current_student, get_current_librarian

router = APIRouter(prefix="/book-requests", tags=["Book Requests"])

@router.post("/", response_model=BookRequestOut)
def submit_request(data: BookRequestCreate, db: Session = Depends(get_db), current_user=Depends(get_current_student)):
    return create_book_request(db, current_user.id, data.title, data.author, data.isbn, data.remarks)

@router.get("/", response_model=List[BookRequestOut])
def get_requests(db: Session = Depends(get_db), _=Depends(get_current_librarian)):
    return list_book_requests(db)

@router.get("/{request_id}", response_model=BookRequestOut)
def get_request(request_id: int, db: Session = Depends(get_db), _=Depends(get_current_librarian)):
    req = get_book_request(db, request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    return req

@router.patch("/{request_id}/approve", response_model=BookRequestOut)
def approve_request(request_id: int, db: Session = Depends(get_db), _=Depends(get_current_librarian)):
    req = update_book_request_status(db, request_id, "approved")
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    return req

@router.patch("/{request_id}/reject", response_model=BookRequestOut)
def reject_request(request_id: int, db: Session = Depends(get_db), _=Depends(get_current_librarian)):
    req = update_book_request_status(db, request_id, "rejected")
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    return req