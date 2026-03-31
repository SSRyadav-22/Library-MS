from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.security import decode_access_token
from app.crud.user import get_user

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    user = get_user(db, payload["user_id"])
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")
    return user

def get_current_librarian(current_user=Depends(get_current_user)):
    if current_user.role != "librarian":
        raise HTTPException(status_code=403, detail="Librarian access required")
    return current_user

def get_current_student(current_user=Depends(get_current_user)):
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Student access required")
    return current_user