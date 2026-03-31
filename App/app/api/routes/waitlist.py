from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.issue import WaitlistCreate, WaitlistOut
from app.crud.issue import get_book_waitlist
from app.services.issue_service import join_waitlist
from app.api.deps import get_current_student, get_current_librarian, get_current_user
from app.db.models import Waitlist

router = APIRouter(prefix="/waitlist", tags=["Waitlist"])

@router.post("/join", response_model=WaitlistOut)
def join(data: WaitlistCreate, db: Session = Depends(get_db), current_user=Depends(get_current_student)):
    return join_waitlist(db, current_user.id, data.book_id)

@router.get("/book/{book_id}", response_model=List[WaitlistOut])
def view_waitlist(book_id: int, db: Session = Depends(get_db), _=Depends(get_current_librarian)):
    return get_book_waitlist(db, book_id)

@router.delete("/cancel/{entry_id}")
def cancel_waitlist(entry_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    entry = db.query(Waitlist).filter(Waitlist.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Waitlist entry not found")
    if current_user.role == "student" and entry.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Cannot cancel another student's waitlist entry")
    db.delete(entry)
    remaining = db.query(Waitlist).filter(
        Waitlist.book_id == entry.book_id
    ).order_by(Waitlist.position).all()
    for i, e in enumerate(remaining, start=1):
        e.position = i
    db.commit()
    return {"message": "Waitlist entry cancelled"}