from . import Base
from app.models.history import Histories
from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
)


class Products(Base, Histories):
    __tablename__ = 'products'
    id = Column(String, primary_key=True)
    category_id = Column(String, ForeignKey('categories.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    title = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    condition = Column(String, nullable=False)          # condition == new/used/soft_delete
    image = Column(String, nullable=False)
    product_detail = Column(String, nullable=True, server_default="None")
    size = Column(String, nullable=True, server_default="S, M, L, XL")
