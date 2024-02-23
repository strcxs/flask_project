from . import Base
from app.models.history import Histories
from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
)


class Carts(Base, Histories):
    __tablename__ = 'carts'
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    product_id = Column(String, ForeignKey('products.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    size = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)