# import uuid
# from flask import request
# from sqlalchemy import (
#     update,
#     delete,
#     insert,
#     select,
# )
# from werkzeug.security import (
#     generate_password_hash,
#     check_password_hash,
# )
# from app.utils.query import run_query
# from app.utils.format_datetime import format_datetime
# from app.utils.auth_token import encode_auth_token
# from app.utils.response import (
#     error_message,
#     success_message,
# )
# from app.models.user import Users
# from . import sign_up_bp, sign_in_bp


# @sign_up_bp.route("", methods=["POST"])
# def sign_up():
#     body = request.json
#     id = uuid.uuid4()
#     name = body["name"]
#     email = body["email"]
#     number = body["number"]
#     password = body["password"]
#     type = body["type"]
    
#     #for testing only
#     if {"email":""+email+""} in run_query(f"select email from users where type ='{type}'"):
#         return "email already exist",401
    
#     else:
#         # run_query("delete from users",True)
#         run_query(f"insert into users (id,name,email,phone_number,password,create_by,type) values ('{id}','{name}','{email}','{number}','{password}','admin','{type}')",True)
#         return "Success, User Created",200
        

    
# @sign_in_bp.route("", methods=["POST"])
# def sign_in():
# <<<<<<< HEAD
#     body = request.json
#     email = body["email"]
#     password = body["password"]
    
#     check = run_query(f"select email,password from users where email = '{email}' and password = '{password}'")
#     query = run_query(f"select name,email,phone_number,type from users where email = '{email}' and password = '{password}'")
#     id = run_query(f"select id from users where email = '{email}' and password = '{password}'")
    
#     if check == []:
#         return "email or password is incorrect",400
#     else:
#         return {
#         "user_information": [
#             query
#         ],
#         "token":[
#             id
#         ],
#         "message":[
#             "Login Success"   
#         ]
#     },200
# =======
#     # For example only
#     name = request.get_json()["name"]
#     user_id = run_query(select(Users.id).where(Users.name==name))[0]["id"]
#     token = encode_auth_token(user_id)
#     return success_message(200, data="Login success", key="message", tkn=token)
# >>>>>>> c96673e7b4a9de2abb77bd0ffb09e51588878abd

import uuid
import re
from flask import request
from sqlalchemy import (
    update,
    delete,
    insert,
    select,
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)
from app.utils.query import run_query
from app.utils.format_datetime import format_datetime
from app.utils.auth_token import encode_auth_token
from app.utils.response import (
    error_message,
    success_message,
)
from app.models.user import Users
from . import sign_up_bp, sign_in_bp


@sign_up_bp.route("", methods=["POST"])
def sign_up():
    body = request.json
    id = uuid.uuid4()
    pattern_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    pass_hash = generate_password_hash(body["password"])

    if ("name" not in body) or (body["name"] == ''):
        return error_message(400, "name can't be empty")
    elif ("email" not in body) or (body["email"] == ''):
        return error_message(400, "email can't be empty")
    elif ("phone_number" not in body) or (body["phone_number"] == ''):
        return error_message(400, "phone_number can't be empty")
    elif ("password" not in body) or (body["password"] == ''):
        return error_message(400, "password can't be empty")
    elif re.match(pattern_email, body["email"]) == False:
        return error_message(400, "invalid email")
    elif any(val.isnumeric() for val in body["phone_number"]) == False:
        return error_message(400, "phone_number must fill with number")
    elif len(body["password"]) < 8:
        return error_message(400, "password must contain at least 8 characters")
    elif len([val for val in body["password"] if val.islower()]) < 1:
        return error_message(400, "Password must contain a lowercase letter")
    elif len([val for val in body["password"] if val.isupper()]) < 1:
        return error_message(400, "Password must contain an uppercase letter")
    elif any(val.isnumeric() for val in body["password"]) == False:
        return error_message(400, "Password must contain a number")
    elif run_query(select(Users.email).where(Users.email==body["email"] and Users.password==pass_hash)):
        return error_message(409, f"email '{body['email']}' already used")
    else:
        run_query(insert(Users).values(id=id, name=body["name"], email=body["email"], phone_number=body["phone_number"], password=pass_hash, create_at=format_datetime(), create_by=body["name"]), True)
        return success_message(201, msg_a="success, user created")


@sign_in_bp.route("", methods=["POST"])
def sign_in():
    body = request.json

    if ("email" not in body) or (body["email"] == ''):
        return error_message(400, "email can't be empty")
    if ("password" not in body) or (body["password"] == ''):
        return error_message(400, "password can't be empty")

    pass_hash = generate_password_hash(body["password"])
    user = run_query(select(Users.email, Users.password).where(Users.email==body["email"] and Users.password==pass_hash))

    try:
        user[0]
    except Exception:
        return error_message(400, "email or password is wrong, your account not found")

    if (run_query(select(Users.email).distinct().where(Users.email==body["email"] and Users.password==pass_hash)) != []) and (check_password_hash(user[0]['password'], body["password"]) == True):
        query = run_query(select(Users.name, Users.email, Users.phone_number, Users.type).where(Users.email==body["email"] and Users.password==pass_hash))[0]
        user_id = run_query(select(Users.id).where(Users.email==body["email"] and Users.password==pass_hash))[0]["id"]
        token = encode_auth_token(user_id)
        return success_message(200, data=query, key="user_information", msg_a="Login success", tkn=token)
    else:
        return error_message(401, "email or password is wrong")
