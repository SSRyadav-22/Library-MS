from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.user import UserOut
from app.crud.user import list_users, get_user
from app.api.deps import get_current_librarian

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=List[UserOut])
def get_all_users(role: str = None, db: Session = Depends(get_db), _=Depends(get_current_librarian)):
    return list_users(db, role)

@router.get("/{user_id}", response_model=UserOut)
def get_user_detail(user_id: int, db: Session = Depends(get_db), _=Depends(get_current_librarian)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user