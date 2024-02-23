import uuid
from flask import request
from sqlalchemy import select
from app.utils.query import run_query
from app.utils.response import (
    error_message,
    success_message,
)
from app.models.product import Products
from app.models.category import Categories
from app.models.image import Images
from . import home_bp


@home_bp.route("/banner", methods=["GET"])
def get_image():
    query = run_query(select(Images.id, Images.title).where(Images.title.like("banner%")).limit(5))
    for val in query:
        val["image"] = f"/image/{val['title']}"
    return success_message(200, data=query)


@home_bp.route("/category", methods=["GET"])
def get_category():
    query = run_query(select(Categories.id, Categories.title).where(Categories.status=="available"))

    for i in query:
        img = run_query(select(Products.image).where(Products.category_id==i["id"], Products.condition!="soft_delete").limit(1))
        if img != []:
            i["image"] = img[0]["image"]
    
    val = [j for j in query if "image" in j]

    return success_message(200, data=val)
