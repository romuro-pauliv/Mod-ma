# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                             API.json.auth.login.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from API.secure.token.IPT_token import IPToken
from flask import request, current_app
from API.status import *
# |--------------------------------------------------------------------------------------------------------------------|

def send_token_after_login(username: str) -> dict[str]:
    return IPToken.token_generate(
        request.remote_addr, username, current_app.config["SECRET_KEY"]
    ), HTTP_202_ACCEPTED