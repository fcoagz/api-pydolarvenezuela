import secrets
from datetime import datetime
from sqlalchemy.orm import Session
from .models import User
from .schemas import UserSchema

user_schema = UserSchema()

def is_user_valid(session: Session, token: str) -> bool:
    user = session.query(User).filter(User.token == token).first()
    if user:
        return user.is_premium
    return False

def create_user(session: Session, name: str) -> str:
    token = f'Bearer {secrets.token_urlsafe(16)}'
    session.add(User(name=name, token=token, is_premium=True, created_at=datetime.now()))
    session.commit()

    return token

def modificate_user(session: Session, id: int, is_premium: bool) -> None:
    session.query(User).filter(User.id == id).update({
        "is_premium": is_premium
    })
    session.commit()

def delete_user(session: Session, id: int) -> None:
    session.query(User).filter(User.id == id).delete()
    session.commit()

def get_users(session: Session) -> list:
    models = session.query(User).all()
    users = user_schema.dump(models, many=True)
    return users

def delete_page(session: Session, name: str) -> None:
    from pyDolarVenezuela.data.models import Page, Monitor, MonitorPriceHistory

    page = session.query(Page).filter(Page.name == name).first()
    if not page:
        raise Exception("La pagina no fue encontrada.")
    
    monitors = session.query(Monitor).filter(Monitor.page_id == page.id).all()
    for monitor in monitors:
        session.query(MonitorPriceHistory).filter(MonitorPriceHistory.monitor_id == monitor.id).delete()
    session.query(Monitor).filter(Monitor.page_id == page.id).delete()
    session.query(Page).filter(Page.name == name).delete()
    session.commit()