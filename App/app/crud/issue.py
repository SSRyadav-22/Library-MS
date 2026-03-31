from sqlalchemy.orm import Session
from app.db.models import IssuedBook, Waitlist, BookRequest
from datetime import datetime, timezone

def get_active_loan(db: Session, user_id: int, book_id: int):
    return db.query(IssuedBook).filter(
        IssuedBook.user_id == user_id,
        IssuedBook.book_id == book_id,
        IssuedBook.status.in_(["issued", "overdue"])
    ).first()

def get_loan(db: Session, loan_id: int):
    return db.query(IssuedBook).filter(IssuedBook.id == loan_id).first()

def list_loans(db: Session, status: str = None):
    query = db.query(IssuedBook)
    if status:
        query = query.filter(IssuedBook.status == status)
    return query.all()

def get_student_loans(db: Session, user_id: int):
    return db.query(IssuedBook).filter(IssuedBook.user_id == user_id).all()

def get_overdue_loans(db: Session):
    now = datetime.now(timezone.utc)
    return db.query(IssuedBook).filter(
        IssuedBook.due_date < now,
        IssuedBook.return_date == None
    ).all()

# Waitlist
def get_waitlist_entry(db: Session, user_id: int, book_id: int):
    return db.query(Waitlist).filter(
        Waitlist.user_id == user_id,
        Waitlist.book_id == book_id
    ).first()

def get_next_in_waitlist(db: Session, book_id: int):
    return db.query(Waitlist).filter(
        Waitlist.book_id == book_id
    ).order_by(Waitlist.position).first()

def get_book_waitlist(db: Session, book_id: int):
    return db.query(Waitlist).filter(
        Waitlist.book_id == book_id
    ).order_by(Waitlist.position).all()

def get_max_position(db: Session, book_id: int):
    result = db.query(Waitlist).filter(Waitlist.book_id == book_id).count()
    return result

# Book Requests
def create_book_request(db: Session, user_id: int, title: str, author: str, isbn: str = None, remarks: str = None):
    req = BookRequest(user_id=user_id, title=title, author=author, isbn=isbn, remarks=remarks)
    db.add(req)
    db.commit()
    db.refresh(req)
    return req

def list_book_requests(db: Session):
    return db.query(BookRequest).all()

def get_book_request(db: Session, request_id: int):
    return db.query(BookRequest).filter(BookRequest.id == request_id).first()

def update_book_request_status(db: Session, request_id: int, status: str):
    req = get_book_request(db, request_id)
    if req:
        req.status = status
        db.commit()
        db.refresh(req)
    return req