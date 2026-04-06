from fastapi import FastAPI
from database import engine, SessionLocal
import models
from models import User
from utils.security import hash_password

from routes import users, transactions, view

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# 🔥 CREATE DEFAULT ADMIN
def create_default_admin():
    db = SessionLocal()

    admin = db.query(User).filter(User.email == "admin@gmail.com").first()

    if not admin:
        new_admin = User(
            email="admin@gmail.com",
            password=hash_password("Admin@123"),
            role="admin"
        )
        db.add(new_admin)
        db.commit()
        print("✅ Default admin created")

    db.close()


# 🔥 CALL FUNCTION WHEN SERVER STARTS
create_default_admin()


# Include routers
app.include_router(users.router)
app.include_router(transactions.router)
app.include_router(view.router)