from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from app.db.models import IssuedBook, Book, Waitlist
from app.crud.issue import get_active_loan, get_loan, get_next_in_waitlist, get_waitlist_entry

LOAN_PERIOD_DAYS = 7
FINE_PER_DAY = 5  # rupees

def issue_book(db: Session, user_id: int, book_id: int):
    # Lock the book row to prevent double checkout
    book = db.query(Book).with_for_update().filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if not book.is_active:
        raise HTTPException(status_code=400, detail="Book is not active")

    # Check if student already has this book
    existing_loan = get_active_loan(db, user_id, book_id)
    if existing_loan:
        raise HTTPException(status_code=400, detail="Student already has an active loan for this book")

    # Check availability
    if book.available_copies <= 0:
        raise HTTPException(status_code=400, detail="No copies available. Please join the waitlist.")

    # Create the loan
    issue_date = datetime.now(timezone.utc)
    due_date = issue_date + timedelta(days=LOAN_PERIOD_DAYS)

    loan = IssuedBook(
        user_id=user_id,
        book_id=book_id,
        issue_date=issue_date,
        due_date=due_date,
        status="issued"
    )
    db.add(loan)

    # Decrement available copies
    book.available_copies -= 1

    db.commit()
    db.refresh(loan)
    return loan


def return_book(db: Session, loan_id: int):
    loan = get_loan(db, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    if loan.status == "returned":
        raise HTTPException(status_code=400, detail="Book already returned")

    # Calculate fine
    return_date = datetime.now(timezone.utc)
    due_date = loan.due_date.replace(tzinfo=timezone.utc) if loan.due_date.tzinfo is None else loan.due_date
    overdue_days = max((return_date - due_date).days, 0)
    fine = overdue_days * FINE_PER_DAY

    # Update loan record
    loan.return_date = return_date
    loan.fine_amount = fine
    loan.status = "returned"

    # Lock the book and check waitlist
    book = db.query(Book).with_for_update().filter(Book.id == loan.book_id).first()
    next_in_queue = get_next_in_waitlist(db, loan.book_id)

    if next_in_queue:
        # Issue directly to next student in waitlist
        new_due_date = return_date + timedelta(days=LOAN_PERIOD_DAYS)
        new_loan = IssuedBook(
            user_id=next_in_queue.user_id,
            book_id=loan.book_id,
            issue_date=return_date,
            due_date=new_due_date,
            status="issued"
        )
        db.add(new_loan)
        db.delete(next_in_queue)
        # Reorder remaining waitlist positions
        remaining = db.query(Waitlist).filter(
            Waitlist.book_id == loan.book_id
        ).order_by(Waitlist.position).all()
        for i, entry in enumerate(remaining, start=1):
            entry.position = i
    else:
        # No waitlist, restore the copy
        book.available_copies += 1

    db.commit()
    db.refresh(loan)

    return {
        "message": "Book returned successfully",
        "fine_amount": fine,
        "overdue_days": overdue_days,
        "return_date": return_date
    }


def join_waitlist(db: Session, user_id: int, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book.available_copies > 0:
        raise HTTPException(status_code=400, detail="Copies are available. Please issue directly.")

    active_loan = get_active_loan(db, user_id, book_id)
    if active_loan:
        raise HTTPException(status_code=400, detail="You already have an active loan for this book")

    existing_entry = get_waitlist_entry(db, user_id, book_id)
    if existing_entry:
        raise HTTPException(status_code=400, detail="You are already in the waitlist for this book")

    current_count = db.query(Waitlist).filter(Waitlist.book_id == book_id).count()
    next_position = current_count + 1

    entry = Waitlist(user_id=user_id, book_id=book_id, position=next_position)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry