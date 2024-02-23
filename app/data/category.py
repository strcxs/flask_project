import uuid
from sqlalchemy import (
    insert,
    delete,
)
from app.utils.query import run_query
from app.utils.format_datetime import format_datetime
from app.models.category import Categories


def category_dummy():
    data = [
        'T-shirt/top',
        'Trouser',
        'Sandal',
        'Bag',
    ]

    run_query(delete(Categories), True)

    for category_name in data:
        run_query(
            insert(Categories).values(
                id=uuid.uuid4(),
                title=category_name,
                create_at=format_datetime(),
                create_by="Developer"
            ), True
        )