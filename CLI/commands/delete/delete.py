# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                       CLI.command.delete.delete.py |
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

def database(token: str) -> None:
    # + inputs +
    database: str = input(PRT_USER_DATABASE)
    
    # + header build +
    header: dict[str] = {"Authorization": f"Bearer {token}"}
    
    # + json +
    json_body: dict[str] = {"database": database}
    
    # + request +
    try:
        rtn = requests.delete(f"{ROUTE_ROOT}{ROUTE_DELETE_DATABASE}", headers=header, json=json_body)
    except requests.exceptions.ConnectionError:
        connection_error()
    
    if rtn.status_code == HTTP_202_ACCEPTED:
        successfully(rtn.text, rtn.status_code)
    else:
        unsuccessful(rtn.text, rtn.status_code)


def collection(token: str) -> None:
    # + inputs +
    database: str = input(PRT_USER_DATABASE)
    collection: str = input(PRT_USER_COLLECTION)
    
    # + header build +
    header: dict[str] = {"Authorization": f"Bearer {token}"}
    
    # + json +
    json_body: dict[str] = {"database": database, "collection": collection}
    
    # + request +
    try:
        rtn = requests.delete(f"{ROUTE_ROOT}{ROUTE_DELETE_COLLLECTION}", headers=header, json=json_body)
    except requests.exceptions.ConnectionError:
        connection_error()
    
    if rtn.status_code == HTTP_202_ACCEPTED:
        successfully(rtn.text, rtn.status_code)
    else:
        unsuccessful(rtn.text, rtn.status_code)


def document(token: str) -> None:
    # + inputs +
    database: str = input(PRT_USER_DATABASE)
    collection: str = input(PRT_USER_COLLECTION)
    doc_id: str = input(PRT_USER_ID)
    
    # + header build +
    header: dict[str] = {"Authorization": f"Bearer {token}"}
    
    # + json +
    json_body: dict[str] = {"database": database, "collection": collection, "doc_id": doc_id}
    
    # + request +
    try:
        rtn = requests.delete(f"{ROUTE_ROOT}{ROUTE_DELETE_DOCUMENT}", headers=header, json=json_body)
    except requests.exceptions.ConnectionError:
        connection_error()
        
    if rtn.status_code == HTTP_202_ACCEPTED:
        successfully(rtn.text, rtn.status_code)
    else:
        unsuccessful(rtn.text, rtn.status_code)
