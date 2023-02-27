# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                 API.routes.auth.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# + imports +----------------------------------------------------------------------------------------------------------+
from API.auth.register import exec_register
from API.auth.login import exec_login
from API.secure.token.IPT_token import required_token
from API.iam.standard_privileges import IAM as AddPrivileges
from API.secure.pam.pam import PAM
from API.log.auth.decorator import LogAuth

from flask import Blueprint, request
# +--------------------------------------------------------------------------------------------------------------------+


standard_privileges = AddPrivileges.StandardPrivileges()
bp = Blueprint('auth', __name__, url_prefix='/auth')


# Register route |-----------------------------------------------------------------------------------------------------|
@bp.route("/register", methods=['POST'])
@standard_privileges.add
def Register() -> tuple[dict[str], int]:
    return exec_register(request.headers.get("Register"))
# |--------------------------------------------------------------------------------------------------------------------|

# Login route |--------------------------------------------------------------------------------------------------------|
@bp.route("/login", methods=['POST'])
@LogAuth.login
def Login() -> tuple[dict[str], int]:
    return exec_login(request.headers.get("Authorization"))

# Identity Access Managment |------------------------------------------------------------------------------------------|
@bp.route("/iam", methods=["PUT"])
@required_token
def IamUpdate() -> None:
    return PAM(request.json).update()
# |--------------------------------------------------------------------------------------------------------------------|
