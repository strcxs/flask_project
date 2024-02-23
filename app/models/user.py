from . import Base
from app.models.history import Histories
from sqlalchemy import (
    Column,
    String,
    Boolean,
    Integer,
)


class Users(Base, Histories):
    __tablename__ = 'users'
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    password = Column(String, nullable=False)
    address = Column(String, nullable=True, server_default="None")
    city = Column(String, nullable=True, server_default="None")
    type = Column(String, nullable=True, server_default="buyer")            # type = seller/buyer  ==> default=buyer
    is_admin = Column(Boolean, nullable=True, server_default="False")
    balance = Column(Integer, nullable=True, server_default="0")