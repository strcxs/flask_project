from . import Base
from app.models.history import Histories
from sqlalchemy import (
    Column,
    String,
)


class Images(Base, Histories):
    __tablename__ = 'images'
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    image = Column(String, nullable=False)