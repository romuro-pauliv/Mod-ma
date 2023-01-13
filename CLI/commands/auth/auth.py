# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                           CLI.command.auth.auth.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from commands.auth.tools_ import *
from route import *
from http_status import *
from commands.auth.p_string import *

import requests
import json
import os
# |--------------------------------------------------------------------------------------------------------------------|


def login() -> dict[str]:
    # + inputs +
    username: str = input(PRT_USER_USERNAME)
    password: str = input(PRT_USER_PASSWORD)

    # + header build +
    header: dict[str] = {"Authorization": header_base64_login(username, password)}

    # + request +
    try:
        rtn = requests.post(f"{ROUTE_ROOT}{ROUTE_LOGIN}", headers=header)
    except requests.exceptions.ConnectionError:
        return connection_error()

    # + sys +
    if rtn.status_code == HTTP_202_ACCEPTED:
        os.system("clear")
        login_successfully("LOGIN SUCCESSFULLY", rtn.status_code)
        return {"username": username, "token": json.loads(rtn.text)["token"]}
    else:
        unsuccessful_login(rtn.text, rtn.status_code)