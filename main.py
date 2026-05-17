from fastapi import FastAPI
from database import engine, SessionLocal
import models
from models import User
from utils.security import hash_password

from routes import users, transactions, view

# Create FastAPI app
app = FastAPI()


# ==============================
# CREATE DATABASE TABLES
# ==============================
try:
    models.Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")

except Exception as e:
    print("❌ Database creation error:", e)


# ==============================
# CREATE DEFAULT ADMIN
# ==============================
def create_default_admin():
    try:
        db = SessionLocal()

        admin = db.query(User).filter(
            User.email == "admin@gmail.com"
        ).first()

        if not admin:
            new_admin = User(
                email="admin@gmail.com",
                password=hash_password("Admin@123"),
                role="admin"
            )

            db.add(new_admin)
            db.commit()

            print("✅ Default admin created")

        else:
            print("✅ Admin already exists")

        db.close()

    except Exception as e:
        print("❌ Admin creation error:", e)


# ==============================
# RUN STARTUP TASKS
# ==============================
try:
    create_default_admin()

except Exception as e:
    print("❌ Startup error:", e)


# ==============================
# INCLUDE ROUTERS
# ==============================
try:
    app.include_router(users.router)
    app.include_router(transactions.router)
    app.include_router(view.router)

    print("✅ Routers loaded successfully")

except Exception as e:
    print("❌ Router loading error:", e)


# ==============================
# ROOT ENDPOINT
# ==============================
@app.get("/")
def home():
    return {
        "message": "Finance Processing API Running Successfully"
    }