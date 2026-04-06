from models import User


def create_user(db, email, password, role):
    user = User(email=email, password=password, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user