
# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                 API.routes.auth.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# + imports +----------------------------------------------------------------------------------------------------------+
from flask import Blueprint, request
from API.auth import register
from API.status import *
from API.crud import read
# +--------------------------------------------------------------------------------------------------------------------+

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route("/register", methods=['POST'])
def REGISTER() -> tuple[str, int]:
    username_request: str = request.json["username"]
    password_request: str = request.json['password']
    email_request: str = request.json['email']
    return register(email_request, username_request, password_request)