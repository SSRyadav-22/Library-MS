from sqlalchemy.orm import Session
from app.db.models import Book

def create_book(db: Session, title: str, author: str, total_copies: int, isbn: str = None):
    book = Book(
        title=title,
        author=author,
        isbn=isbn,
        total_copies=total_copies,
        available_copies=total_copies
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

def get_book(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()

def list_books(db: Session, active_only: bool = True):
    query = db.query(Book)
    if active_only:
        query = query.filter(Book.is_active == True)
    return query.all()

def update_book(db: Session, book_id: int, updates: dict):
    book = get_book(db, book_id)
    if not book:
        return None
    for key, value in updates.items():
        if value is not None:
            setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book

def delete_book(db: Session, book_id: int):
    book = get_book(db, book_id)
    if book:
        book.is_active = False
        db.commit()
    return book