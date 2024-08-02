import secrets
from datetime import datetime
from sqlalchemy.orm import Session
from .models import User

def is_user_valid(session: Session, token: str) -> bool:
    user = session.query(User).filter(User.token == token).first()
    if user:
        if user.is_premium:
            return True
    return False

def create_user(session: Session, name: str) -> None:
    token = f'Bearer {secrets.token_urlsafe(16)}'
    session.add(User(name=name, token=token, is_premium=True, created_at=datetime.now()))
    session.commit()

def modificate_user(session: Session, id: int, is_premium: bool) -> None:
    session.query(User).filter(User.id == id).update({
        "is_premium": is_premium
    })
    session.commit()

def delete_user(session: Session, id: int) -> None:
    session.query(User).filter(User.id == id).delete()
    session.commit()

def get_users(session: Session) -> list:
    users = []
    models = session.query(User).all()
    for model in models:
        user_dict = {
            column.name: getattr(model, column.name)
            for column in model.__table__.columns
        }
        users.append(user_dict)
    return users