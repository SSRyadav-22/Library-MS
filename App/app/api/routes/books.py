from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.book import BookCreate, BookUpdate, BookOut, BookAvailability
from app.crud.book import create_book, get_book, list_books, update_book, delete_book
from app.crud.issue import get_book_waitlist
from app.api.deps import get_current_librarian, get_current_user
from app.db.models import IssuedBook

router = APIRouter(prefix="/books", tags=["Books"])

@router.post("/", response_model=BookOut)
def add_book(book_data: BookCreate, db: Session = Depends(get_db), _=Depends(get_current_librarian)):
    return create_book(db, book_data.title, book_data.author, book_data.total_copies, book_data.isbn)

@router.get("/", response_model=List[BookOut])
def get_books(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return list_books(db)

@router.get("/catalog/all", response_model=List[BookAvailability])
def catalog(db: Session = Depends(get_db), _=Depends(get_current_user)):
    books = list_books(db, active_only=True)
    result = []
    for book in books:
        expected_return = None
        if book.available_copies == 0:
            nearest_loan = db.query(IssuedBook).filter(
                IssuedBook.book_id == book.id,
                IssuedBook.status.in_(["issued", "overdue"])
            ).order_by(IssuedBook.due_date).first()
            if nearest_loan:
                expected_return = nearest_loan.due_date

        waitlist_count = len(get_book_waitlist(db, book.id))

        result.append(BookAvailability(
            id=book.id,
            title=book.title,
            author=book.author,
            isbn=book.isbn,
            available_copies=book.available_copies,
            total_copies=book.total_copies,
            expected_return_date=expected_return,
            waitlist_count=waitlist_count
        ))
    return result

@router.get("/{book_id}", response_model=BookOut)
def get_book_detail(book_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    book = get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.patch("/{book_id}", response_model=BookOut)
def edit_book(book_id: int, updates: BookUpdate, db: Session = Depends(get_db), _=Depends(get_current_librarian)):
    book = update_book(db, book_id, updates.model_dump(exclude_none=True))
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.delete("/{book_id}")
def remove_book(book_id: int, db: Session = Depends(get_db), _=Depends(get_current_librarian)):
    book = delete_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deactivated successfully"}