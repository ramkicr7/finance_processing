from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Transaction
from collections import defaultdict

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def allow_view(role: str):
    if role not in ["viewer", "analyst", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied")


# GET ALL TRANSACTIONS
@router.get("/transactions")
def get_transactions(role: str, db: Session = Depends(get_db)):
    allow_view(role)
    return db.query(Transaction).all()


# FILTER TRANSACTIONS
@router.get("/transactions/filter")
def filter_transactions(
    role: str,
    type: str = None,
    category: str = None,
    db: Session = Depends(get_db)
):
    allow_view(role)

    query = db.query(Transaction)

    if type:
        query = query.filter(Transaction.type == type)

    if category:
        query = query.filter(Transaction.category == category)

    return query.all()


# DASHBOARD SUMMARY
@router.get("/summary")
def summary(role: str, db: Session = Depends(get_db)):
    allow_view(role)

    data = db.query(Transaction).all()

    income = sum(r.amount for r in data if r.type == "income")
    expense = sum(r.amount for r in data if r.type == "expense")

    return {
        "total_income": income,
        "total_expense": expense,
        "balance": income - expense
    }


# CATEGORY-WISE ANALYSIS
@router.get("/summary/category")
def category_summary(role: str, db: Session = Depends(get_db)):
    allow_view(role)

    data = db.query(Transaction).all()
    result = defaultdict(int)

    for r in data:
        if r.type == "expense":
            result[r.category] += r.amount

    return result


# RECENT TRANSACTIONS
@router.get("/transactions/recent")
def recent(role: str, db: Session = Depends(get_db)):
    allow_view(role)

    return db.query(Transaction).order_by(Transaction.id.desc()).limit(5).all()