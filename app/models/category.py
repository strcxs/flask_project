from . import Base
from app.models.history import Histories
from sqlalchemy import (
    Column,
    String,
)


class Categories(Base, Histories):
    __tablename__ = 'categories'
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    status = Column(String, nullable=True, server_default="available")          # condition == available/soft_delete