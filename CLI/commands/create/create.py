# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                       CLI.command.create.create.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from routes.route import *
from data.http_status import *
from commands.create.p_string import *

import requests

from typing import Any
# |--------------------------------------------------------------------------------------------------------------------|
def database(token: str) -> None:
    # + inputs +
    database: str = input(PRT_USER_DATABASE)

    # + header build +
    header: dict[str] = {"Authorization": f'Bearer {token}'}

    # + json +
    json_data: dict[str, Any] = {"database": database}

    # + request +
    try:
        rtn = requests.post(f"{ROUTE_ROOT}{ROUTE_DATABASE}", headers=header, json=json_data)
    except requests.exceptions.ConnectionError:
        return connection_error()
    
    # + sys +
    if rtn.status_code == HTTP_201_CREATED:
        successfully(json.loads(rtn.text)["response"], rtn.status_code)
    else:
        unsuccessful(json.loads(rtn.text)["response"], rtn.status_code)


def collection(token: str) -> None:
    # + inputs +
    database: str = input(PRT_USER_DATABASE)
    collection: str = input(PRT_USER_COLLECTION)

    # + header build +
    header: dict[str] = {"Authorization": f'Bearer {token}'}

    # + json +
    json_data: dict[str, Any] = {"database": database, "collection": collection}

    # + request +
    try:
        rtn = requests.post(f"{ROUTE_ROOT}{ROUTE_COLLECTION}", headers=header, json=json_data)
    except requests.exceptions.ConnectionError:
        return connection_error()
    
    # + sys +
    if rtn.status_code == HTTP_201_CREATED:
        successfully(json.loads(rtn.text)["response"], rtn.status_code)
    else:
        unsuccessful(json.loads(rtn.text)["response"], rtn.status_code)


def document(token: str) -> None:
    # + inputs +
    database: str = input(PRT_USER_DATABASE)
    collection: str = input(PRT_USER_COLLECTION)
    document: str = input(PRT_USER_DOCUMENT)
    
    # + json treatment +
    try:
        document: dict[str, Any] = json.loads(document)
    except json.decoder.JSONDecodeError:
        unsuccessful("JSON SYNTAX ERROR", 400)

    # + header build +
    header: dict[str] = {"Authorization": f'Bearer {token}'}

    # + json +
    json_data: dict[str, Any] = {"database": database, "collection": collection, "document": document}
    
    # + request +
    try:
        rtn = requests.post(f"{ROUTE_ROOT}{ROUTE_DOCUMENT}", headers=header, json=json_data)
    except requests.exceptions.ConnectionError:
        return connection_error()
    
    # + sys +
    if rtn.status_code == HTTP_201_CREATED:
        successfully(json.loads(rtn.text)["response"]['_id'], rtn.status_code)
    else:
        unsuccessful(rtn.text, rtn.status_code)