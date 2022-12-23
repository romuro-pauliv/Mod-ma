
# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                 API.routes.auth.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# + imports +----------------------------------------------------------------------------------------------------------+
from flask import Blueprint, request, current_app
from API.auth import register, login, read_authentication, token_generate
from API.status import *
from typing import Union
from API.log import LogAuth
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
@LogAuth.login_route
def LOGIN() -> tuple[str, int]:
    
    # decode auth base64 |---------------------------------------------------------------------------------------------|
    auth_list: auth_list_typing = read_authentication(request.headers.get("Authorization"))
    if auth_list[1] == HTTP_400_BAD_REQUEST:
        return auth_list
    # |----------------------------------------------------------------------------------------------------------------|

    # Verify in database the user/password |---------------------------------------------------------------------------|
    login_db: tuple[str, int] = login(username=auth_list[0], password=auth_list[1])
    if login_db[1] == HTTP_403_FORBIDDEN:
        return login_db
    # |----------------------------------------------------------------------------------------------------------------|

    return token_generate(auth_list[0], key_api=current_app.config['SECRET_KEY']), HTTP_202_ACCEPTED
# |--------------------------------------------------------------------------------------------------------------------|
