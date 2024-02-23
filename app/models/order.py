from . import Base
from app.models.history import Histories
from sqlalchemy import (
    Column,
    String,
    Integer,
    JSON,
    ForeignKey,
)


class Orders(Base, Histories):
    __tablename__ = 'orders'
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    shipping_method = Column(String, nullable=False)            # shipping_method = "Same day" atau "Regular"/"Next day"
    shipping_address = Column(JSON, nullable=False)
    status = Column(String, nullable=True, server_default="waiting")     # status = waiting/processed/delivered/arrived
    total_price = Column(Integer, nullable=False)