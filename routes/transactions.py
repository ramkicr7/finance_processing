from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Transaction
from schemas import TransactionCreate, TransactionUpdate

router = APIRouter()


# 🔌 DB CONNECTION
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔐 ROLE CHECK FUNCTIONS

def admin_only(role: str):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")


def analyst_or_admin(role: str):
    if role not in ["analyst", "admin"]:
        raise HTTPException(status_code=403, detail="Only analyst/admin allowed")


def all_roles(role: str):
    if role not in ["viewer", "analyst", "admin"]:
        raise HTTPException(status_code=403, detail="Invalid role")


# 🟢 CREATE TRANSACTION
@router.post("/transactions")
def create_transaction(data: TransactionCreate, user_id: int, role: str, db: Session = Depends(get_db)):
    admin_only(role)

    t = Transaction(
        amount=data.amount,
        type=data.type,
        category=data.category,
        date=data.date,
        notes=data.notes,
        user_id=user_id
    )

    db.add(t)
    db.commit()
    db.refresh(t)

    return {"msg": "Transaction added", "data": t}


# 🔵 VIEW TRANSACTIONS (WITH DATE FILTER 🔥)
@router.get("/transactions")
def get_transactions(
    user_id: int,
    role: str,
    start_date: str = None,
    end_date: str = None,
    db: Session = Depends(get_db)
):
    all_roles(role)

    query = db.query(Transaction).filter(Transaction.user_id == user_id)

    # 🔥 DATE FILTER
    if start_date and end_date:
        query = query.filter(
            Transaction.date >= start_date,
            Transaction.date <= end_date
        )

    return query.all()


# 🟡 UPDATE TRANSACTION
@router.put("/transactions/{id}")
def update_transaction(id: int, data: TransactionUpdate, user_id: int, role: str, db: Session = Depends(get_db)):
    admin_only(role)

    t = db.query(Transaction).filter(
        Transaction.id == id,
        Transaction.user_id == user_id
    ).first()

    if not t:
        raise HTTPException(status_code=404, detail="Transaction not found")

    if data.amount is not None:
        t.amount = data.amount
    if data.category is not None:
        t.category = data.category
    if data.notes is not None:
        t.notes = data.notes

    db.commit()
    db.refresh(t)

    return {"msg": "Transaction updated", "data": t}


# 🔴 DELETE TRANSACTION
@router.delete("/transactions/{id}")
def delete_transaction(id: int, user_id: int, role: str, db: Session = Depends(get_db)):
    admin_only(role)

    t = db.query(Transaction).filter(
        Transaction.id == id,
        Transaction.user_id == user_id
    ).first()

    if not t:
        raise HTTPException(status_code=404, detail="Transaction not found")

    db.delete(t)
    db.commit()

    return {"msg": "Transaction deleted"}


# 🟣 ADMIN VIEW ALL
@router.get("/admin/transactions")
def get_all_transactions(role: str, db: Session = Depends(get_db)):
    admin_only(role)
    return db.query(Transaction).all()


# 🟠 SUMMARY
@router.get("/summary")
def summary(user_id: int, role: str, db: Session = Depends(get_db)):
    analyst_or_admin(role)

    transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()

    total_income = sum(t.amount for t in transactions if t.type == "income")
    total_expense = sum(t.amount for t in transactions if t.type == "expense")

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": total_income - total_expense
    }


# 🔥 ANALYSIS
@router.get("/analysis")
def analyze_user(user_id: int, role: str, db: Session = Depends(get_db)):

    if role != "analyst":
        raise HTTPException(status_code=403, detail="Analyst only")

    transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()

    total_income = sum(t.amount for t in transactions if t.type == "income")
    total_expense = sum(t.amount for t in transactions if t.type == "expense")

    category_spending = {}
    for t in transactions:
        if t.type == "expense":
            category_spending[t.category] = category_spending.get(t.category, 0) + t.amount

    top_category = max(category_spending, key=category_spending.get) if category_spending else None

    tips = []

    if total_expense > total_income:
        tips.append("⚠️ You are spending more than you earn")

    if top_category == "food":
        tips.append("🍔 Reduce food expenses")

    if top_category == "shopping":
        tips.append("🛍️ Reduce shopping expenses")

    if total_income > total_expense:
        tips.append("✅ Good savings habits! Keep it up")

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": total_income - total_expense,
        "top_spending_category": top_category,
        "tips": tips
    }