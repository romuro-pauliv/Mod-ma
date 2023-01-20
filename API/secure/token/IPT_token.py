# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                      API.secure.token.IPT_token.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, request

from typing import Union, Callable, Any

from API.status import *

import datetime
import jwt

# |--------------------------------------------------------------------------------------------------------------------|


class IPToken(object):
    # | TOKEN GENERATE |===============================================================================================|
    @staticmethod
    def token_generate(ip_addr: str, username: str, key_api: str) -> dict[str]:
        # pack assembly |----------------------------------------------------------------------------------------------|
        encode_dict: dict[str, Union[str, datetime.datetime]] = {
            "hash": generate_password_hash(ip_addr),
            "username": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=20)
        }
        # |------------------------------------------------------------------------------------------------------------|

        # token encode |-----------------------------------------------------------------------------------------------|
        token: str = jwt.encode(payload=encode_dict, key=key_api, algorithm="HS256")
        # |------------------------------------------------------------------------------------------------------------|

        return {"token": token, "token expiration time [UTC]": encode_dict["exp"].strftime("%m/%d/%Y %H:%M:%S")}
    # |================================================================================================================|
    
    # | TOKEN AUTHENTICATION |=========================================================================================|
    @staticmethod
    def token_authentication(token: str, ip_addr: str, key_api: str) -> tuple[str, int]:
        try:
            try:
                token: str = token.split()[1]
            except IndexError:
                return "BAD REQUEST - COLON ERROR", HTTP_400_BAD_REQUEST
        except AttributeError:
            return "BAD REQUEST - NO DATA", HTTP_400_BAD_REQUEST
        # decode token |-----------------------------------------------------------------------------------------------|
        try:
            try:
                decode_token: dict = jwt.decode(token, key_api, ['HS256'])
            except jwt.exceptions.DecodeError:
                return "INVALID TOKEN", HTTP_400_BAD_REQUEST
        except jwt.exceptions.ExpiredSignatureError:
            return "EXPIRED TOKEN", HTTP_403_FORBIDDEN
        # |------------------------------------------------------------------------------------------------------------|

        # ip hash validation |-----------------------------------------------------------------------------------------|
        if not check_password_hash(decode_token['hash'], ip_addr):
            return "IP ADDRESS DOES NOT MATCH", HTTP_403_FORBIDDEN
        # |------------------------------------------------------------------------------------------------------------|

        return "VALID TOKEN", HTTP_200_OK
    # |================================================================================================================|
    
    class Tools(object):
        # | GET USERNAME PER TOKEN |===================================================================================|
        @staticmethod
        def get_username_per_token(token: str) -> None:
            # Only useful with the required_token decorator. Without the decorator, it is possible that many exceptions 
            # will be generated because the token validation is in the decorator.
            token: str = token.split()[1]
            decode_token: dict = jwt.decode(token, current_app.config["SECRET_KEY"], ['HS256'])
            return decode_token['username']
        # |============================================================================================================|

# REQUIRED TOKEN |=====================================================================================================|
def required_token(func: Callable[..., Any]) -> Callable[..., tuple[str, int] | Any]:
    def wrapper(*args, **kwargs) -> tuple[str, int] | Any:
        # token authentication |---------------------------------------------------------------------------------------|
        token: str = request.headers.get("Authorization")
        ip: str = request.remote_addr
        token_auth: tuple[str, int] = IPToken.token_authentication(token, ip, current_app.config["SECRET_KEY"])
        if token_auth[1] != HTTP_200_OK:
            return token_auth
        # |------------------------------------------------------------------------------------------------------------|
        return func(*args, **kwargs)

    # Renaming the function name:
    wrapper.__name__ = func.__name__
    return wrapper
# |====================================================================================================================|