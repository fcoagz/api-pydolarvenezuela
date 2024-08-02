from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id              = Column(Integer, primary_key=True)
    name            = Column(String, nullable=False)
    token           = Column(String(16), nullable=False)
    is_premium      = Column(Boolean, default=False)
    created_at      = Column(DateTime, nullable=False)