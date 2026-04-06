from pydantic import BaseModel, EmailStr, validator
from typing import Optional
import re
from enum import Enum


# ---------- ROLE ENUM (DROPDOWN) ----------

class RoleEnum(str, Enum):
    admin = "admin"
    viewer = "viewer"
    analyst = "analyst"


# ---------- USER ----------

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: RoleEnum

    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")

        if not re.search(r"[A-Z]", v):
            raise ValueError("Must include uppercase letter")

        if not re.search(r"[a-z]", v):
            raise ValueError("Must include lowercase letter")

        if not re.search(r"\d", v):
            raise ValueError("Must include a number")

        if not re.search(r"[!@#$%^&*]", v):
            raise ValueError("Must include special character")

        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: RoleEnum   # ✅ use enum here also

    class Config:
        from_attributes = True


# ---------- TRANSACTION ----------

class TransactionCreate(BaseModel):
    amount: float
    type: str
    category: str
    date: str
    notes: Optional[str] = None

    @validator("type")
    def validate_type(cls, v):
        if v.lower() not in ["income", "expense"]:
            raise ValueError("Type must be 'income' or 'expense'")
        return v.lower()


class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    category: Optional[str] = None
    notes: Optional[str] = None


class TransactionResponse(BaseModel):
    id: int
    amount: float
    type: str
    category: str
    date: str
    notes: Optional[str]

    class Config:
        from_attributes = True
        
class TransactionCreate(BaseModel):
    amount: float

    @validator("amount")
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError("Amount must be positive")
        return v    