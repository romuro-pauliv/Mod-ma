# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                           CLI.command.auth.auth.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from commands.auth.tools_ import *
from routes.route import *
from data.http_status import *
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
        successfully("LOGIN SUCCESSFULLY", rtn.status_code)
        return {"username": username, "token": json.loads(rtn.text)["token"]}
    else:
        unsuccessful(rtn.text, rtn.status_code)


def register() -> dict[str]:
    # + inputs +
    username: str = input(PRT_USER_USERNAME)
    password: str = input(PRT_USER_PASSWORD)
    email: str = input(PRT_USER_EMAIL)

    # + header build +
    header: dict[str] = {"Register": header_base64_register(username, password, email)}

    # + request +
    try:
        rtn = requests.post(f"{ROUTE_ROOT}{ROUTE_REGISER}", headers=header)
    except requests.exceptions.ConnectionError:
        return connection_error()
    
    # + sys +
    if rtn.status_code == HTTP_201_CREATED:
        os.system("clear")
        successfully("SUCCESSFULLY REGISTERED", rtn.status_code)
    else:
        unsuccessful(rtn.text, rtn.status_code)