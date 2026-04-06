from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime
from database import Base
from sqlalchemy.orm import relationship
from datetime import datetime


# 👤 USER TABLE
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    # 🔗 Relationship
    transactions = relationship("Transaction", back_populates="owner", cascade="all, delete")


# 💰 TRANSACTION TABLE
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)  # income / expense
    category = Column(String, nullable=False)
    date = Column(String, nullable=False)
    notes = Column(String)

    # 🔥 NEW FEATURES
    is_deleted = Column(Boolean, default=False)   # soft delete
    created_at = Column(DateTime, default=datetime.utcnow)

    # 🔗 Foreign Key
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # 🔗 Relationship
    owner = relationship("User", back_populates="transactions")