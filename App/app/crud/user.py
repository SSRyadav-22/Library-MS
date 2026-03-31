from sqlalchemy.orm import Session
from app.db.models import User
from app.core.security import get_password_hash

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, name: str, email: str, password: str, role: str):
    hashed = get_password_hash(password)
    user = User(name=name, email=email, password_hash=hashed, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def list_users(db: Session, role: str = None):
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    return query.all()