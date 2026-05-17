from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal
from models import User
from schemas import (
    UserCreate,
    UserLogin,
    UserResponse
)
from utils.security import (
    hash_password,
    verify_password
)

router = APIRouter()


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ==========================================
# CREATE USER
# ==========================================

@router.post("/users")
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db)
):

    # Prevent multiple admins
    if data.role == "admin":

        existing_admin = db.query(User).filter(
            User.role == "admin"
        ).first()

        if existing_admin:
            raise HTTPException(
                status_code=400,
                detail="Admin already exists"
            )

    # Check existing email
    existing_user = db.query(User).filter(
        User.email == data.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    # Create new user
    user = User(
        email=data.email,
        password=hash_password(data.password),
        role=data.role
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "User created successfully",
        "user_id": user.id,
        "role": user.role
    }


# ==========================================
# LOGIN USER
# ==========================================

@router.post("/login")
def login(
    data: UserLogin,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == data.email
    ).first()

    # User not found
    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    # Wrong password
    if not verify_password(
        data.password,
        user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Wrong password"
        )

    return {
        "message": "Login successful",
        "user_id": user.id,
        "role": user.role
    }


# ==========================================
# GET ALL USERS
# ==========================================

@router.get(
    "/users",
    response_model=List[UserResponse]
)
def get_users(
    db: Session = Depends(get_db)
):

    users = db.query(User).all()

    return users