from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.issue import IssueCreate, IssueOut, ReturnOut
from app.crud.issue import list_loans, get_loan, get_student_loans, get_overdue_loans
from app.services.issue_service import issue_book, return_book
from app.api.deps import get_current_librarian, get_current_user

router = APIRouter(prefix="/loans", tags=["Loans"])

@router.post("/issue", response_model=IssueOut)
def issue(data: IssueCreate, db: Session = Depends(get_db), _=Depends(get_current_librarian)):
    return issue_book(db, data.user_id, data.book_id)

@router.post("/{loan_id}/return", response_model=ReturnOut)
def return_loan(loan_id: int, db: Session = Depends(get_db), _=Depends(get_current_librarian)):
    return return_book(db, loan_id)

@router.get("/overdue", response_model=List[IssueOut])
def overdue_loans(db: Session = Depends(get_db), _=Depends(get_current_librarian)):
    return get_overdue_loans(db)

@router.get("/student/{user_id}", response_model=List[IssueOut])
def student_loans(user_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return get_student_loans(db, user_id)

@router.get("/", response_model=List[IssueOut])
def get_loans(status: str = None, db: Session = Depends(get_db), _=Depends(get_current_librarian)):
    return list_loans(db, status)

@router.get("/{loan_id}", response_model=IssueOut)
def loan_detail(loan_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    loan = get_loan(db, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan