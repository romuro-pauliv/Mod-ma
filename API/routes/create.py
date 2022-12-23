# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                               API.routes.create.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|


# imports |------------------------------------------------------------------------------------------------------------|
from API.status import *
from typing import Union
from flask import Blueprint, request, current_app
from API.auth import token_authentication
# |--------------------------------------------------------------------------------------------------------------------|

bp = Blueprint('create', __name__, url_prefix='/create')

# Create database |----------------------------------------------------------------------------------------------------|
@bp.route('/database', methods=['POST'])
def database() -> tuple[str, int]:
    
    # token authentication |-------------------------------------------------------------------------------------------|
    token: str = request.headers.get("Authorization")
    ip: str = request.remote_addr
    token_auth: tuple[str, int] = token_authentication(token, ip, current_app.config["SECRET_KEY"])
    if token_auth[1] != HTTP_200_OK:
        return token_auth
    # |----------------------------------------------------------------------------------------------------------------|
    
    return 'TEST OK', HTTP_202_ACCEPTED
# |--------------------------------------------------------------------------------------------------------------------|