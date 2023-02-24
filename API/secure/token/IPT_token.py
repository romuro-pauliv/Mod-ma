# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                      API.secure.token.IPT_token.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, request
from functools import wraps

from typing import Union, Callable, Any

from API.status import *
from API.json.responses.token import token_status

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
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=40)
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
            token: str = token.split()[1]
        except IndexError:
            return token_status.Responses.R4XX.colon_error()
        except AttributeError:
            return token_status.Responses.R4XX.data_error()
        # decode token |-----------------------------------------------------------------------------------------------|
        try:
            decode_token: dict = jwt.decode(token, key_api, ['HS256'])
        except jwt.exceptions.DecodeError:
            return token_status.Responses.R4XX.invalid_token()
        except jwt.exceptions.ExpiredSignatureError:
            return token_status.Responses.R4XX.expired_token()
        # |------------------------------------------------------------------------------------------------------------|

        # ip hash validation |-----------------------------------------------------------------------------------------|
        if not check_password_hash(decode_token['hash'], ip_addr):
            return token_status.Responses.R4XX.ip_error()
        # |------------------------------------------------------------------------------------------------------------|
        return token_status.Responses.R2XX.valid_token()
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
    @wraps(func)
    def wrapper(*args, **kwargs) -> tuple[str, int] | Any:
        # token authentication |---------------------------------------------------------------------------------------|
        token: str = request.headers.get("Authorization")
        ip: str = request.remote_addr
        token_auth: tuple[str, int] = IPToken.token_authentication(token, ip, current_app.config["SECRET_KEY"])
        if token_auth[1] != HTTP_200_OK:
            return token_auth
        # |------------------------------------------------------------------------------------------------------------|
        return func(*args, **kwargs)
    return wrapper
# |====================================================================================================================|