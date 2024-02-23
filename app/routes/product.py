import uuid
import base64
from PIL import Image
from io import BytesIO
from flask import request
from sqlalchemy import (
    update,
    delete,
    insert,
    select,
    and_,
)
# from app.utils.classification.postprocessing import search_product
from app.utils.query import run_query
from app.utils.format_datetime import format_datetime
from app.utils.auth_token import decode_auth_token
from app.utils.response import (
    error_message,
    success_message,
)
from app.models.user import Users
from app.models.product import Products
from app.models.category import Categories
from app.models.image import Images
from . import products_bp


# ==========================================================================
# For testing only, to get all products
@products_bp.route("/all", methods=["GET"])
def get_category_all():
    q = run_query(select(Products))
    return success_message(200, data=q)
# ==========================================================================


# First save image to model Images, then for column images url in model product fill the endpoint image
@products_bp.route("", methods=["POST"])
@decode_auth_token
def create_product(current_user):
    body = request.get_json()

    if run_query(select(Users.id).where(Users.id==current_user)) == []:
        return error_message(400, "User not found")
    elif run_query(select(Users.is_admin).where(Users.id==current_user)) == [{"is_admin": False}]:
        return error_message(403, "Unauthorized user")
    elif ("category" not in body) or (body["category"] == ""):
        return error_message(400, "Category can't empty, please check your request!")
    elif type(body["category"]) != str:
        return error_message(400, "Type of category must be string")
    elif run_query(select(Categories.id).where(Categories.id==body["category"], Categories.status=="available")) == []:
        return error_message(400, "Category not found")
    elif ("product_name" not in body) or (body["product_name"] == ""):
        return error_message(400, "Product_name can't empty, please check your request!")
    elif type(body["product_name"]) != str:
        return error_message(400, "Type of product_name must be string")
    elif ("price" not in body) or (body["price"] == "") or (body["price"] == None):
        return error_message(400, "Price can't empty, please check your request!")
    elif type(body["price"]) != int:
        return error_message(400, "Type of price must be number or integer")
    elif body["price"] < 1:
        return error_message(400, "Price must be positive numbers")
    elif ("condition" not in body) or (body["condition"] == ""):
        return error_message(400, "Condition can't empty, please check your request!")
    elif type(body["condition"]) != str:
        return error_message(400, "Type of condition must be string")
    elif (body["condition"] != "new") and (body["condition"] != "used"):
        return error_message(400, "Fill condition with only 'new' or 'used'")
    elif ("images" not in body) or (body["images"] == ""):
        return error_message(400, "Images can't empty, please check your request!")
    elif ("description" not in body) or (body["description"] == ""):
        return error_message(400, "Description can't empty, please check your request!")
    elif run_query(select(Products.title, Products.category_id, Products.condition).distinct().where(and_(Products.title==body["product_name"], Products.category_id==body["category"], Products.condition==body["condition"]))) == [{"title": body["product_name"], "category_id": body["category"], "condition": body["condition"]}]:
        return error_message(409, f"Product '{body['product_name']}' already exist")
    elif run_query(select(Products.title, Products.category_id).distinct().where(and_(Products.title==body["product_name"], Products.category_id==body["category"], Products.condition=="soft_delete"))) == [{"title": body["product_name"], "category_id": body["category"]}]:
        user_name = run_query(select(Users.name).where(Users.id==current_user))[0]["name"]
        image_name = f"{body['product_name']}-{body['category']}-{body['condition']}-{uuid.uuid4()}.jpg"
        run_query(insert(Images).values(id=uuid.uuid4(), title=image_name, image=body["images"], create_at=format_datetime(), create_by=user_name), True)
        run_query(update(Products).values(price=body["price"], condition=body["condition"], image=f"/image/{image_name}", product_detail=body["description"], create_at=format_datetime(), create_by=user_name).where(and_(Products.title==body["product_name"], Products.category_id==body["category"], Products.condition=='soft_delete')), True)
        return success_message(201, msg=f"Product '{body['product_name']}' added")
    else:
        user_name = run_query(select(Users.name).where(Users.id==current_user))[0]["name"]
        image_name = f"{body['product_name']}-{body['category']}-{body['condition']}-{uuid.uuid4()}.jpg"
        run_query(insert(Images).values(id=uuid.uuid4(), title=image_name, image=body["images"], create_at=format_datetime(), create_by=user_name), True)
        run_query(insert(Products).values(id=uuid.uuid4(), category_id=body["category"], title=body["product_name"], price=body["price"], condition=body["condition"], image=f"/image/{image_name}", product_detail=body["description"], create_at=format_datetime(), create_by=user_name), True)
        return success_message(201, msg=f"Product '{body['product_name']}' added")


@products_bp.route("", methods=["GET"])
def get_product_list():
    params = request.args
    page = params.get("page", default=1, type=int)
    page_size = params.get("page_size", default=50, type=int)
    sort_by = params.get("sort_by", default="Price a_z", type=str)
    category = params.get("category")
    price = params.get("price")
    condition = params.get("condition", type=str)
    product_name = params.get("product_name", type=str)

    sort = 'ASC'
    where = ""

    if sort_by == "Price z_a": sort = 'DESC'
    elif (sort_by != "") and (sort_by != "Price z_a") and (sort_by != "Price a_z"):
        return error_message(400, "Params sort_by unknown, please use 'Price z_a' or 'Price a_z'")

    if product_name != "" and product_name != None:
        where += f"title LIKE '%{product_name}%' and "

    if category != "" and category != None:
        cat_arr = category.split(",")
        cat = ""
        if len(cat_arr) > 1:
            for i in cat_arr:
                cat += f"'{i}',"
            where += f"category_id IN ({cat.removesuffix(',')}) and "
        else:
            where += f"category_id = '{category}' and "
        cat = ""

    if condition != "" and condition != None:
        cond_arr = condition.split(",")
        cond = ""
        if len(cond_arr) > 1:
            for i in cond_arr:
                cond += f"'{i}',"
            where += f"condition IN ({cond.removesuffix(',')}) and "
        else:
            where += f"condition = '{condition}' and "
        cond = ""

    if price != "" and price != None:
        price_arr = price.split(",")
        where += f"price>='{price_arr[0]}' and price<='{price_arr[1]}' and "

    query = run_query(
        f"""SELECT id, image, title, price
            FROM products
            WHERE {where} condition!='soft_delete'
            ORDER BY price {sort}
            LIMIT {page_size}
        """
    )
    where = ""
    return success_message(200, data=query, row=True)


@products_bp.route("", methods=["PUT"])
@decode_auth_token
def update_product(current_user):
    body = request.get_json()

    if run_query(select(Users.id).where(Users.id==current_user)) == []:
        return error_message(400, "User not found")
    elif run_query(select(Users.is_admin).where(Users.id==current_user)) == [{"is_admin": False}]:
        return error_message(403, "Unauthorized user")
    elif ("product_name" not in body) or (body["product_name"] == ""):
        return error_message(400, "Product_name can't empty, please check your request!")
    elif type(body["product_name"]) != str:
        return error_message(400, "Type of product_name must be string")
    elif ("product_id" not in body) or (body["product_id"] == ""):
        return error_message(400, "Product_id can't empty, please check your request!")
    elif type(body["product_id"]) != str:
        return error_message(400, "Type of product_id must be string")
    elif (run_query(select(Products.id).where(Products.id==body["product_id"], Products.condition!='soft_delete')) == []) or (run_query(select(Products.condition).where(Products.id==body["product_id"])) == [{"condition": "soft_delete"}]):
        return error_message(400, "Product not found")
    elif ("category" not in body) or (body["category"] == ""):
        return error_message(400, "Category can't empty, please check your request!")
    elif type(body["category"]) != str:
        return error_message(400, "Type of category must be string")
    elif run_query(select(Categories.id).where(Categories.id==body["category"], Categories.status=="available")) == []:
        return error_message(400, "Category not found")
    elif ("price" not in body) or (body["price"] == "") or (body["price"] == None):
        return error_message(400, "Price can't empty, please check your request!")
    elif type(body["price"]) != int:
        return error_message(400, "Type of price must be number or integer")
    elif body["price"] < 1:
        return error_message(400, "Price must be positive numbers, please check your request!")
    elif ("condition" not in body) or (body["condition"] == ""):
        return error_message(400, "Condition can't empty, please check your request!")
    elif type(body["condition"]) != str:
        return error_message(400, "Type of condition must be string")
    elif (body["condition"] != "new") and (body["condition"] != "used"):
        return error_message(400, "Fill condition with only 'new' or 'used', please check your request!")
    elif ("description" not in body) or (body["description"] == ""):
        return error_message(400, "Description can't empty, please check your request!")
    elif ("images" not in body) or (body["images"] == ""):
        return error_message(400, "Images can't empty, please check your request!")
    elif run_query(select(Products.title, Products.category_id, Products.condition, Products.price, Products.image, Products.product_detail).distinct().where(and_(Products.title==body["product_name"], Products.category_id==body["category"], Products.condition==body["condition"]))) == [{"title": body["product_name"], "category_id": body["category"], "condition": body["condition"], "price": body["price"], "image":body["images"], "product_detail":body["description"]}]:
        return error_message(409, "Product already exist")
    else:
        user_name = run_query(select(Users.name).where(Users.id==current_user))[0]["name"]
        image_name = f"{body['product_name']}-{body['category']}-{body['condition']}-{uuid.uuid4()}.jpg"
        run_query(insert(Images).values(id=uuid.uuid4(), title=image_name, image=body["images"], create_at=format_datetime(), create_by=user_name), True)
        run_query(update(Products).values(id=body["product_id"], category_id=body["category"], title=body["product_name"], price=body["price"], condition=body["condition"], image=f"/image/{image_name}", product_detail=body["description"], update_at=format_datetime(), update_by=user_name).where(and_(Products.id==body["product_id"], Products.condition!="soft_delete")), True)
        return success_message(200, msg="Product updated")


@products_bp.route("/<product_id>", methods=["DELETE"])
@decode_auth_token
def delete_product(current_user, product_id):
    if run_query(select(Users.id).where(Users.id==current_user)) == []:
        return error_message(400, "User not found")
    elif run_query(select(Users.is_admin).where(Users.id==current_user)) == [{"is_admin": False}]:
        return error_message(403, "Unauthorized user")
    elif (run_query(select(Products.id).where(Products.id==product_id and Products.condition!='soft_delete')) == []) or (run_query(select(Products.condition).where(Products.id==product_id)) == [{"condition": "soft_delete"}]):
        return error_message(400, "Product not found")
    else:
        user_name = run_query(select(Users.name).where(Users.id==current_user))[0]["name"]
        product_name = run_query(select(Products.title).where(Products.id==product_id))[0]["title"]
        run_query(update(Products).values(condition="soft_delete", update_at=format_datetime(), update_by=user_name).where(Products.id==product_id and Products.condition!="soft_delete"), True)
        return success_message(200, msg=f"Product '{product_name}' deleted")


@products_bp.route("/search_image", methods=["POST"])
def search_product_by_image():
    body = request.get_json()
    # img_decode = Image.open(BytesIO(base64.b64decode(body["image"])))

    # img = search_product(img_decode)
    img = "T-shirt/top"
    query = run_query(select(Categories.id).where(Categories.title==img))[0]["id"]

    # val = [i["id"] for i in query]
    return success_message(200, key="category_id", data=query)


@products_bp.route("/<product_id>", methods=["GET"])
def get_product_details(product_id):
    query = run_query(select(Products.id, Products.title, Products.size, Products.product_detail, Products.price, Products.image).where(Products.id==product_id))
    if query != []:
        query[0]["images_url"] = query[0].pop("image")
        query[0]["images_url"] = [query[0]["images_url"]]
        query[0]["size"] = query[0]["size"].split(",")
        return success_message(200, data=query[0])
    else:
        return success_message(200, data={
                "id": "",
                "images_url": [],
                "price": 0,
                "product_detail": "",
                "size": [],
                "title": ""
            }
        )
