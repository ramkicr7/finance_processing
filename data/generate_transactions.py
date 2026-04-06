import random
from datetime import datetime, timedelta
from database import SessionLocal
from models import Transaction

db = SessionLocal()

# 👥 USERS (based on your data)
user_ids = [2, 3, 4, 5, 6, 7]   # ram, rahul, ajay...

categories = ["food", "rent", "travel", "shopping", "bills", "salary", "upi"]
types = ["income", "expense"]

start_date = datetime(2026, 3, 1)

for user_id in user_ids:   # 🔥 LOOP EACH USER

    for i in range(30):   # 30 days
        date = start_date + timedelta(days=i)

        for _ in range(random.randint(3, 5)):  # 3–5 transactions per day

            t_type = random.choice(types)

            # 💰 REALISTIC AMOUNT LOGIC
            if t_type == "income":
                amount = random.randint(2000, 50000)
                category = "salary"
            else:
                amount = random.randint(50, 2000)
                category = random.choice(["food", "travel", "shopping", "bills"])

            t = Transaction(
                amount=amount,
                type=t_type,
                category=category,
                date=str(date.date()),
                notes=f"{category} payment",
                user_id=user_id   # 🔥 KEY PART
            )

            db.add(t)

db.commit()
db.close()

print("🔥 30 days user-wise transactions generated!")