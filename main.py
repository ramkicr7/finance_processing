from fastapi import FastAPI
from utils.security import hash_password

app = FastAPI()

test = hash_password("Admin123")


@app.get("/")
def home():
    return {
        "message": "Hashing successful"
    }