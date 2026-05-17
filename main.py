from fastapi import FastAPI
from database import engine, SessionLocal

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Database import successful"
    }