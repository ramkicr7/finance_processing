from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from utils.security import hash_password, verify_password
from schemas import UserCreate, UserLogin
from typing import List
from schemas import UserResponse

router = APIRouter()


# 🔌 DB CONNECTION
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🟢 CREATE USER
@router.post("/users")
def create_user(data: UserCreate, db: Session = Depends(get_db)):

    # prevent multiple admins
    if data.role == "admin":
        existing_admin = db.query(User).filter(User.role == "admin").first()
        if existing_admin:
            raise HTTPException(status_code=400, detail="Admin already exists")

    # check existing email
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(
        email=data.email,
        password=hash_password(data.password),
        role=data.role
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "msg": "User created",
        "role": user.role
    }


# 🔵 LOGIN
@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Wrong password")

    return {
        "msg": "Login successful",
        "role": user.role,
        "user_id": user.id   # 🔥 VERY IMPORTANT
    }


# 🟣 GET ALL USERS (TO KNOW user_id)
@router.get("/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()