# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                           CLI.command.read.read.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from routes.route import *
from data.http_status import *
from commands.read.p_string import *


from typing import Union
import requests
import json
import os
# |--------------------------------------------------------------------------------------------------------------------|


def database(token: str) -> None:
    # + header build +
    header: dict[str] = {"Authorization": f'Bearer {token}'}

    # + request +
    try:
        rtn = requests.get(f"{ROUTE_ROOT}{ROUTE_READ_DATABASE}", headers=header)
    except requests.exceptions.ConnectionError:
        return connection_error()
    
    # + sys +
    if rtn.status_code == HTTP_200_OK:
        database_list(rtn.text)
    else:
        unsuccessful(rtn.text, rtn.status_code)

def collection(token: str) -> None:
    # + inputs +
    database: str = input(PRT_USER_DATABASE)

    # + header build +
    header: dict[str] = {"Authorization": f'Bearer {token}'}

    # + json build +
    json_data: dict[str] = {"database": database}

    # + request +
    try:
        rtn = requests.get(f"{ROUTE_ROOT}{ROUTE_READ_COLLECTION}", headers=header, json=json_data)
    except requests.exceptions.ConnectionError:
        return connection_error()
    
    # + sys +
    if rtn.status_code == HTTP_200_OK:
        collection_list(rtn.text)
    else:
        unsuccessful(rtn.text, rtn.status_code)