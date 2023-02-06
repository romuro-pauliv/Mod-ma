# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                       CLI.command.update.update.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from routes.route import *
from data.http_status import *
from commands.update.p_string import *

from typing import Union, Any
import requests
# |--------------------------------------------------------------------------------------------------------------------|

def document(token: str) -> None:
    # + inputs +
    database: str = input(PRT_USER_DATABASE)
    collection: str = input(PRT_USER_COLLECTION)
    _id: str = input(PRT_USER_ID)
    update: str = input(PRT_USER_UPDATE)
    
    # + json treatment +
    try:
        update: dict[str, Any] = json.loads(update)
    except json.decoder.JSONDecodeError:
        unsuccessful("JSON SYNTAX ERROR", 400)
    
    # + header build +
    header: dict[str] = {"Authorization": f"Bearer {token}"}
    
    # + json +
    json_body: dict[str, Any] = {
        "database": database, "collection": collection,
        "_id": _id, "update": update
    }
    
    # + request +
    try:
        rtn = requests.put(f"{ROUTE_ROOT}{ROUTE_UPDATE_DOCUMENT}", headers=header, json=json_body)
    except requests.exceptions.ConnectionError:
        return connection_error()
    
    if rtn.status_code == HTTP_202_ACCEPTED:
        successfully(rtn.text, rtn.status_code)
    else:
        unsuccessful(rtn.text, rtn.status_code)