
# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                 API.routes.auth.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# + imports +----------------------------------------------------------------------------------------------------------+
from flask import Blueprint, request
from API.auth import register, login, read_authentication
from API.status import *
import base64
from typing import Union
# +--------------------------------------------------------------------------------------------------------------------+

# | type hint |--------------------------------------------------------------------------------------------------------|
auth_list_typing = Union[list[str], list[str, int]]
# |--------------------------------------------------------------------------------------------------------------------|


bp = Blueprint('auth', __name__, url_prefix='/auth')


# Register route |-----------------------------------------------------------------------------------------------------|
@bp.route("/register", methods=['POST'])
def REGISTER() -> tuple[str, int]:
    username_request: str = request.json["username"]
    password_request: str = request.json['password']
    email_request: str = request.json['email']
    return register(email_request, username_request, password_request)
# |--------------------------------------------------------------------------------------------------------------------|

# Login route |--------------------------------------------------------------------------------------------------------|
@bp.route("/login", methods=['POST'])
def LOGIN() -> tuple[str, int]:
    auth_list: auth_list_typing = read_authentication(request.headers.get("Authorization"))
    if auth_list[1] == HTTP_400_BAD_REQUEST:
        return auth_list
    return login(username=auth_list[0], password=auth_list[1])
# |--------------------------------------------------------------------------------------------------------------------|