from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(Text, nullable=False)
    role = Column(String(20), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint("role IN ('librarian', 'student')", name="chk_user_role"),
    )

    issued_books = relationship("IssuedBook", back_populates="user")
    waitlist_entries = relationship("Waitlist", back_populates="user")
    book_requests = relationship("BookRequest", back_populates="user")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    author = Column(String(255), nullable=False)
    isbn = Column(String(20), unique=True, nullable=True)
    total_copies = Column(Integer, nullable=False)
    available_copies = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint("total_copies >= 0", name="chk_total_copies"),
        CheckConstraint("available_copies >= 0", name="chk_available_copies"),
        CheckConstraint("available_copies <= total_copies", name="chk_available_le_total"),
    )

    issued_books = relationship("IssuedBook", back_populates="book")
    waitlist_entries = relationship("Waitlist", back_populates="book")


class IssuedBook(Base):
    __tablename__ = "issued_books"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    issue_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    due_date = Column(DateTime(timezone=True), nullable=False)
    return_date = Column(DateTime(timezone=True), nullable=True)
    fine_amount = Column(Integer, default=0)
    status = Column(String(20), nullable=False, default="issued")

    __table_args__ = (
        CheckConstraint("fine_amount >= 0", name="chk_fine_amount"),
        CheckConstraint("status IN ('issued', 'returned', 'overdue')", name="chk_issue_status"),
    )

    user = relationship("User", back_populates="issued_books")
    book = relationship("Book", back_populates="issued_books")


class Waitlist(Base):
    __tablename__ = "waitlist"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    position = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="waitlist_entries")
    book = relationship("Book", back_populates="waitlist_entries")


class BookRequest(Base):
    __tablename__ = "book_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    isbn = Column(String(20), nullable=True)
    remarks = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint("status IN ('pending', 'approved', 'rejected')", name="chk_request_status"),
    )

    user = relationship("User", back_populates="book_requests")