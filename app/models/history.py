from sqlalchemy import (
    Column,
    String,
)


class Histories():
    create_at = Column(String, nullable=False)
    create_by = Column(String, nullable=False)
    update_at = Column(String, nullable=True, server_default="None")
    update_by = Column(String, nullable=True, server_default="None")