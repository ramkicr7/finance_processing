import sys
import os

# 🔥 Fix import path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal
from models import User
from utils.security import hash_password

db = SessionLocal()

# 👨‍💼 Analyst names
analysts = ["analyst1", "analyst2", "analyst3"]

for name in analysts:
    user = User(
        email=f"{name}@gmail.com",
        password=hash_password("Analyst@123"),
        role="analyst"   # 🔥 IMPORTANT
    )
    db.add(user)

db.commit()
db.close()

print("✅ Analyst users created")