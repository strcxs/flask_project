import uuid
from flask import request
from sqlalchemy import (
    update,
    delete,
    insert,
    select,
    alias,
    func
)
from app.utils.query import run_query
from app.utils.format_datetime import format_datetime
from app.utils.auth_token import decode_auth_token
from app.utils.response import (
    error_message,
    success_message,
)
from app.models.category import Categories
from app.models.user import Users
from app.models.product import Products
from app.models.cart import Carts
from . import cart_bp, shipping_price_bp


@cart_bp.route("", methods=["POST"])
@decode_auth_token
def add_to_cart(current_user):
    body = request.json
    product_id = body.get("id")
    quantity = body.get("quantity")
    size = body.get("size") 
    user_name = run_query(select(Users.name).where(Users.id==current_user))[0]["name"]

    if product_id == "" or quantity == "" or size == "":
        return error_message(400,"invalid product")
    if run_query(select(Carts.product_id, Carts.size).where(Carts.user_id==current_user)) == [{"product_id": product_id, "size": size}]:
        run_query(update(Carts).values(quantity=Carts.quantity+quantity).where(Carts.user_id==current_user), True)
        return success_message(200, msg="Item added to cart, success")
    else:
        run_query(insert(Carts).values(id=uuid.uuid4(),user_id=current_user,product_id=product_id,size=size,quantity=quantity,create_at=format_datetime(),create_by=user_name),True)
        return success_message(201, msg="Item added to cart, success")


@cart_bp.route("", methods=["GET"])
@decode_auth_token
def get_user_carts(current_user):
    result = []
    for x in run_query(select(Carts,Products).filter(Products.id==Carts.product_id).where(Carts.user_id==current_user)):
        result.append({"id":x['id'],"details":{"quantity":x["quantity"],"size":x["size"]},"price":x["price"],"image":x["image"],"name":x["title"]})
    return success_message(200, data=result)


@cart_bp.route("/<cart_id>", methods=["DELETE"])
@decode_auth_token
def delete_cart_item(current_user, cart_id):
    if run_query(select(Carts.user_id).where(Carts.user_id==current_user))!=[]:
        run_query(delete(Carts).where(Carts.id==cart_id),True)
        return success_message(201,msg="Cart deleted")
    if run_query(select(Carts.id).where(Carts.id==cart_id))==[]:
        return error_message(400,"item not found")


# Get shipping price after push data to model ShippingPrice in endpoint add to cart
@shipping_price_bp.route("", methods=["GET"])
@decode_auth_token
def get_shipping_price(current_user):
    cart = run_query(select(Carts).where(Carts.user_id==current_user))

    if cart == []: return error_message(400, "You don't have a cart")
    else:
        shipping_method = [{"name": "regular", "price": 0}, {"name": "next day", "price": 0}]
        products_in_cart = run_query(select(Carts.quantity, Products.price).filter(Products.id==Carts.product_id).where(Carts.user_id==current_user))
        total_price = sum(float(val["price"] * val["quantity"]) for val in products_in_cart)

        regular_price = (15*total_price)/100 if total_price < 200 else (20*total_price)/100
        shipping_method[0]["price"] = int(regular_price)

        next_day_price = (20*total_price)/100 if total_price < 300 else (25*total_price)/100
        shipping_method[1]["price"] = int(next_day_price)

        return success_message(200, data=shipping_method)
