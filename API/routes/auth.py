# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                 API.routes.auth.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# + imports +----------------------------------------------------------------------------------------------------------+
from API.auth.register import exec_register

from API.secure.base.decrypt_base64 import Decrypt
from API.secure.token.IPT_token import IPToken, required_token

from API.iam import Privileges
from API.secure.pam.pam import PAM

from API.log.auth.decorator import LogAuth

from flask import Blueprint, request
# +--------------------------------------------------------------------------------------------------------------------+


privileges = Privileges("admin").NewUser()
bp = Blueprint('auth', __name__, url_prefix='/auth')


# Register route |-----------------------------------------------------------------------------------------------------|
@bp.route("/register", methods=['POST'])
# @privileges.standart_privileges
def REGISTER() -> tuple[dict[str], int]:
    return exec_register(request.headers.get("Register"))
# |--------------------------------------------------------------------------------------------------------------------|

# # Login route |--------------------------------------------------------------------------------------------------------|
# @bp.route("/login", methods=['POST'])
# @LogAuth.login
# def LOGIN() -> tuple[dict, int]:
#     # decode auth base64 |---------------------------------------------------------------------------------------------|
#     auth_list = Decrypt.Base64.read_authentication(request.headers.get("Authorization"), "login")
#     if auth_list[1] == HTTP_400_BAD_REQUEST:
#         return auth_list
#     # |----------------------------------------------------------------------------------------------------------------|

#     # Verify in database the user/password |---------------------------------------------------------------------------|
#     login_db: tuple[str, int] = login(username=auth_list[0], password=auth_list[1])
#     if login_db[1] == HTTP_403_FORBIDDEN:
#         return login_db
#     # |----------------------------------------------------------------------------------------------------------------|
#     return IPToken.token_generate(
#         request.remote_addr,
#         auth_list[0],
#         current_app.config['SECRET_KEY']), HTTP_202_ACCEPTED
# # |--------------------------------------------------------------------------------------------------------------------|

# Identity Access Managment |------------------------------------------------------------------------------------------|
@bp.route("/iam", methods=["PUT"])
@required_token
def IAM_UPDATE() -> None:
    return PAM(request.json).update()
# |--------------------------------------------------------------------------------------------------------------------|
