import uuid
from flask import request
from sqlalchemy import (
    update,
    delete,
    insert,
    select,
)
from app.utils.query import run_query
from app.utils.format_datetime import format_datetime
from app.utils.auth_token import decode_auth_token
from app.utils.response import (
    error_message,
    success_message,
)
from app.models.user import Users
from app.models.product import Products
from app.models.cart import Carts
from app.models.order import Orders
from . import user_bp, sales_bp


@user_bp.route("", methods=["GET"])
@decode_auth_token
def user_details(current_user):
    query = run_query(select(Users.name, Users.email, Users.phone_number).where(Users.id==current_user))[0]
    return success_message(200, data=query)


# Change to model Users
@user_bp.route("/shipping_address", methods=["POST"])
@decode_auth_token
def change_shipping_address(current_user):
    body = request.json
    number = body.get('phone_number')
    city = body.get('city')
    address = body.get('address')
    name = body.get('name')
    user_name = run_query(select(Users.name).where(Users.id==current_user))[0]["name"]

    if city != None:
        run_query(update(Users).values(city=city, update_at=format_datetime(), update_by=user_name).where(Users.id==current_user),True)
    if number != None:
        run_query(update(Users).values(phone_number=number, update_at=format_datetime(), update_by=user_name).where(Users.id==current_user),True)
    if address != None:
        run_query(update(Users).values(address=address, update_at=format_datetime(), update_by=user_name).where(Users.id==current_user),True)
    if name != None:
        run_query(update(Users).values(name=name, update_at=format_datetime(), update_by=user_name).where(Users.id==current_user),True)
    
    if city == None and number == None and address == None and name == None:
        return success_message(200,"nothing has been changed")
    else:
        return success_message(200,"update successfully")

# Get data from model Users
@user_bp.route("/shipping_address", methods=["GET"])
@decode_auth_token
def get_user_shipping_address(current_user):
    query = run_query(select(Users.id,Users.name,Users.phone_number,Users.address,Users.city).where(Users.id==current_user))[0]
    return success_message(200, data=query)


@user_bp.route("/balance", methods=["POST"])
@decode_auth_token
def top_up_balance(current_user):
    body = request.json
    amount = int(body.get('amount'))
    user_name = run_query(select(Users.name).where(Users.id==current_user))[0]["name"]
    
    if amount < 1:
        return error_message(400,"please specify a positive amount")
    elif amount != None:
        run_query(update(Users).values(balance=Users.balance+amount, update_at=format_datetime(), update_by=user_name).where(Users.id==current_user),True)
        return success_message(200,"Top up balance success")
    else:
        return error_message(400,"please input your balance input")


@user_bp.route("/balance", methods=["GET"])
@decode_auth_token
def get_user_balance(current_user):
    query = run_query(select(Users.balance).where(Users.id==current_user))[0]
    return success_message(200, data=query)


@sales_bp.route("", methods=["GET"])
@decode_auth_token
def get_total_sales(current_user):
    query = run_query(select(Users.balance).where(Users.id==current_user, Users.is_admin==True))[0]
    query["total"] = query.pop("balance")
    return success_message(200, data=query)

@user_bp.route("/order", methods=["GET"])
@decode_auth_token
def user_orders(current_user):
    products_result=[]
    for x in run_query(select(Orders)):
        for x in run_query(select(Carts,Products.image,Products.price,Products.name,Products.title).filter(Products.id==Carts.product_id).where(Carts.user_id==current_user)):
            products_result.append({"id":x['id'],"details":{"quantity":x["quantity"],"size":x["size"]},"price":x["price"],"image":x["image"],"name":x["title"]})
        data = {"id":x['id'],"created_at":x['create_at'],"products":products_result,"shipping_method":x['shipping_method'],"shipping_address":x['shipping_address']}
    return success_message(200,data)