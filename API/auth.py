# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                        API.auth.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# +--------------------------------------------------------------------------------------------------------------------+
from werkzeug.security import check_password_hash, generate_password_hash

from .status import *
from .db import get_db
from .validation.register_validation import Register
from .validation.login_validation import Login

from typing import Union, Any, Callable

from bson.objectid import ObjectId
import datetime
import base64
import jwt
from flask import request, current_app
import binascii
# +--------------------------------------------------------------------------------------------------------------------+


class PassException(Exception):
    pass

# REGISTER |===========================================================================================================|
def register(email: str, username: str, password: str) -> tuple[str, int]:
    # tools |----------------------------------------------------------------------------------------------------------|
    tools = Register
    validation = tools.Validation
    # |----------------------------------------------------------------------------------------------------------------|
    # Username, password, and email validation |-----------------------------------------------------------------------|
    func_list: list[Callable[[str], tuple[str, int]]] = [
        validation.username, validation.password, validation.email
    ]
    func_input: list[str] = [username, password, email]
    for n, func in enumerate(func_list):
        func_validation: tuple[str, int] = func(func_input[n])
        if func_validation[1] == HTTP_400_BAD_REQUEST:
            return func_validation
    # |----------------------------------------------------------------------------------------------------------------|

    # Validation in database to verify if not exists the same username or email in database |--------------------------|
    fields: list = ['email', 'username']
    values: list = [email, username]
    try:
        for i in range(2):
            if tools.search_argument(fields[i], values[i]) == False:
                raise PassException
    except PassException:
        return "EMAIL OR USERNAME IN USE", HTTP_403_FORBIDDEN
    # |----------------------------------------------------------------------------------------------------------------|

    # Assemble document |----------------------------------------------------------------------------------------------|
    id_str: str = str(ObjectId())
    json_package: dict[str, str] = {
        "_id": id_str,
        "user": "root",
        "datetime": ["UTC", datetime.datetime.utcnow()],
        "username": username,
        "password": generate_password_hash(password),
        "email": email
    }
    # |----------------------------------------------------------------------------------------------------------------|
    get_db().USERS.REGISTER.insert_one(json_package)    # REGISTER COMPLETE
    return "CREATED", HTTP_201_CREATED
# |====================================================================================================================|

# LOGIN |==============================================================================================================|
def login(username: str, password: str) -> tuple[str, int]:
    # tools |----------------------------------------------------------------------------------------------------------|
    tools = Login
    # |----------------------------------------------------------------------------------------------------------------|
    
    # find password |--------------------------------------------------------------------------------------------------|
    passwd: tuple[str, int] = Login.find_password(username)
    if passwd[1] == HTTP_403_FORBIDDEN:
        return passwd
    # |----------------------------------------------------------------------------------------------------------------|

    # check password |-------------------------------------------------------------------------------------------------|
    if not check_password_hash(passwd[0], password):
        return "INCORRECT USERNAME/PASSWORD", HTTP_403_FORBIDDEN
    # |----------------------------------------------------------------------------------------------------------------|

    return "SUCCESSFULLY", HTTP_202_ACCEPTED
# |====================================================================================================================|

# read base64 |--------------------------------------------------------------------------------------------------------|
def read_authentication(header_auth: str, _method: str) -> list[str]:
    try:
        try:
            try:
                auth: str = header_auth.split()[1]
                login_data: list[str] = base64.b64decode(auth).decode().split(":")

                if _method == "login":
                    if len(login_data) > 2:
                        return "BAD REQUEST - COLON ERROR", HTTP_400_BAD_REQUEST
                if _method == "register":
                    if len(login_data) > 3:
                        return "CHARACTER [:] NOT ALLOWED", HTTP_400_BAD_REQUEST

                if login_data[1]:
                    return login_data
            except IndexError:
                return "BAD REQUEST - NO COLON IDENTIFY", HTTP_400_BAD_REQUEST
        except AttributeError:
            return "BAD REQUEST - NO DATA", HTTP_400_BAD_REQUEST
    except binascii.Error:
        return "BAD REQUEST - BINASCII ERROR", HTTP_400_BAD_REQUEST
# |--------------------------------------------------------------------------------------------------------------------|

# TOKEN |==============================================================================================================|
def token_generate(ip_addr: str, username: str, key_api: str) -> dict[str]:
    # pack assembly |--------------------------------------------------------------------------------------------------|
    encode_dict: dict[str, Union[str, datetime.datetime]] = {
        "hash": generate_password_hash(ip_addr),
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=20)
    }
    # |----------------------------------------------------------------------------------------------------------------|
    
    # token encode |---------------------------------------------------------------------------------------------------|
    token: str = jwt.encode(payload=encode_dict, key=key_api, algorithm="HS256")
    # |----------------------------------------------------------------------------------------------------------------|

    return {"token": token, "token expiration time [UTC]": encode_dict["exp"].strftime("%m/%d/%Y %H:%M:%S")}
# |====================================================================================================================|

# TOKEN AUTHENTICATION |===============================================================================================|
def token_authentication(token: str, ip_addr: str, key_api: str) -> tuple[str, int]:
    try:
        try:
            token: str = token.split()[1]
        except IndexError:
            return "BAD REQUEST - COLON ERROR", HTTP_400_BAD_REQUEST
    except AttributeError:
        return "BAD REQUEST - NO DATA", HTTP_400_BAD_REQUEST
    # decode token |---------------------------------------------------------------------------------------------------|
    try:
        try:
            decode_token: dict = jwt.decode(token, key_api, ['HS256'])
        except jwt.exceptions.DecodeError:
            return "INVALID TOKEN", HTTP_400_BAD_REQUEST
    except jwt.exceptions.ExpiredSignatureError:
        return "EXPIRED TOKEN", HTTP_403_FORBIDDEN
    # |----------------------------------------------------------------------------------------------------------------|

    # ip hash validation |---------------------------------------------------------------------------------------------|
    if not check_password_hash(decode_token['hash'], ip_addr):
        return "IP ADDRESS DOES NOT MATCH", HTTP_403_FORBIDDEN
    # |----------------------------------------------------------------------------------------------------------------|

    return "VALID TOKEN", HTTP_200_OK
# |====================================================================================================================|

# REQUIRED TOKEN |=====================================================================================================|
def required_token(func: Callable[..., Any]) -> Callable[..., tuple[str, int] | Any]:
    def wrapper(*args, **kwargs) -> tuple[str, int] | Any:
        # token authentication |---------------------------------------------------------------------------------------|
        token: str = request.headers.get("Authorization")
        ip: str = request.remote_addr
        token_auth: tuple[str, int] = token_authentication(token, ip, current_app.config["SECRET_KEY"])
        if token_auth[1] != HTTP_200_OK:
            return token_auth
    # |----------------------------------------------------------------------------------------------------------------|
        return func(*args, **kwargs)

    # Renaming the function name:
    wrapper.__name__ = func.__name__
    return wrapper
# |====================================================================================================================|

# GET USERNAME PER TOKEN |---------------------------------------------------------------------------------------------|
def get_username_per_token(token: str) -> None:
    # Only useful with the required_token decorator. Without the decorator, it is possible that many exceptions will be
    # generated because the token validation is in the decorator.
    token: str = token.split()[1]
    decode_token: dict = jwt.decode(token, current_app.config["SECRET_KEY"], ['HS256'])
    return decode_token['username']
    