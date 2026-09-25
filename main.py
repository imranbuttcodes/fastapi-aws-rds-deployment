import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Database Configuration

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# Database Model

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)


# Create tables if they don't already exist
Base.metadata.create_all(bind=engine)


# FastAPI Application

app = FastAPI()


# Request Model

class UserCreate(BaseModel):
    username: str


# Frontend

@app.get("/")
def home():
    return FileResponse("static/index.html")


# GET /users


@app.get("/users")
def get_users():
    db = SessionLocal()

    try:
        users = db.query(User).all()

        return [
            {
                "id": user.id,
                "username": user.username
            }
            for user in users
        ]

    finally:
        db.close()


# POST /users


@app.post("/users")
def create_user(user: UserCreate):
    db = SessionLocal()

    try:
        new_user = User(username=user.username)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "id": new_user.id,
            "username": new_user.username
        }

    finally:
        db.close()


# DELETE /users/{id}

@app.delete("/users/{id}")
def delete_user(id: int):
    db = SessionLocal()

    try:
        user = db.query(User).filter(User.id == id).first()

        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        db.delete(user)
        db.commit()

        return {
            "message": "User deleted successfully"
        }

    finally:
        db.close()

