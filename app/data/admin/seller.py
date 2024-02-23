import uuid
from werkzeug.security import generate_password_hash
from sqlalchemy import (
    insert,
    select
)
from app.utils.query import run_query
from app.utils.format_datetime import format_datetime
from app.models.user import Users


# Insert data admin to database
# Use this, it because nothing endpoint to insert data for admin/seller
# And admin is only one person
def admin_seller():
    check_admin = run_query(
        select(Users).where(
            Users.is_admin==True
        )
    )
    if not check_admin:
        pass_admin = generate_password_hash("GuaAdmin")
        run_query(
            insert(Users).values(
                id=uuid.uuid4(),
                name="Bambang",
                email="bambang2022@gmail.com",
                phone_number="082234821991",
                password=pass_admin,
                type="seller",
                is_admin=True,
                create_at=format_datetime(),
                create_by="Developer",
            ), True
        )