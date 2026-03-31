from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, engine
from app.api.routes import auth, books, issues, waitlist, requests, users

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library Management System",
    description="A role-based library management API built with FastAPI and PostgreSQL",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(books.router)
app.include_router(issues.router)
app.include_router(waitlist.router)
app.include_router(requests.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Library Management System API is running"}