from sqlalchemy import create_engine
from ..consts import URL_DB
from .models import Base

engine = create_engine(URL_DB)
Base.metadata.create_all(engine)