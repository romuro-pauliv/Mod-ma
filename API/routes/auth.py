# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                 API.routes.auth.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# + imports +----------------------------------------------------------------------------------------------------------+
from API.auth import register, login

from API.secure.base.decrypt_base64 import Decrypt
from API.secure.token.IPT_token import IPToken, required_token

from API.status import *

from API.iam import Privileges
from API.secure.pam.pam import PAM

from API.log.auth.decorator import LogAuth

from flask import Blueprint, request, current_app
from typing import Union
# +--------------------------------------------------------------------------------------------------------------------+

# | type hint |--------------------------------------------------------------------------------------------------------|
auth_list_typing = Union[list[str], list[str, int]]
# |--------------------------------------------------------------------------------------------------------------------|

# IAM |----------------------------------------------------------------------------------------------------------------|
privileges = Privileges("admin").NewUser()
# |--------------------------------------------------------------------------------------------------------------------|


bp = Blueprint('auth', __name__, url_prefix='/auth')


# Register route |-----------------------------------------------------------------------------------------------------|
@bp.route("/register", methods=['POST'])
@privileges.standart_privileges
def REGISTER() -> tuple[str, int]:
    register_list: auth_list_typing = Decrypt.Base64.read_authentication(request.headers.get("Register"), "register")
    if register_list[1] == HTTP_400_BAD_REQUEST:
        return register_list
    return register(register_list[2], register_list[0], register_list[1])
# |--------------------------------------------------------------------------------------------------------------------|

# Login route |--------------------------------------------------------------------------------------------------------|
@bp.route("/login", methods=['POST'])
@LogAuth.login
def LOGIN() -> tuple[dict, int]:
    # decode auth base64 |---------------------------------------------------------------------------------------------|
    auth_list: auth_list_typing = Decrypt.Base64.read_authentication(request.headers.get("Authorization"), "login")
    if auth_list[1] == HTTP_400_BAD_REQUEST:
        return auth_list
    # |----------------------------------------------------------------------------------------------------------------|

    # Verify in database the user/password |---------------------------------------------------------------------------|
    login_db: tuple[str, int] = login(username=auth_list[0], password=auth_list[1])
    if login_db[1] == HTTP_403_FORBIDDEN:
        return login_db
    # |----------------------------------------------------------------------------------------------------------------|
    return IPToken.token_generate(
        request.remote_addr,
        auth_list[0],
        current_app.config['SECRET_KEY']), HTTP_202_ACCEPTED
# |--------------------------------------------------------------------------------------------------------------------|

# Identity Access Managment |------------------------------------------------------------------------------------------|
@bp.route("/iam", methods=["GET"])
@required_token
def IAM_UPDATE() -> None:
    return PAM(request.json).test()
# |--------------------------------------------------------------------------------------------------------------------|
