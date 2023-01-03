# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                     test.config.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | imports |----------------------------------------------------------------------------------------------------------|
import json
import base64
import requests
from pymongo import MongoClient
# |--------------------------------------------------------------------------------------------------------------------|

# ROUTES |=============================================================================================================|
root_route: str = "http://127.0.0.1:5000"
login_route: str = "/auth/login"
register_route: str = "/auth/register"
create_database_route: str = "/tests/test-create-database"
create_collection_route: str = "/tests/test-create-collection"
create_document_route: str = "/tests/test-create-document"
# |====================================================================================================================|

# MONGO CLIENT |=======================================================================================================|
mongo = MongoClient()
# |====================================================================================================================|


# PRE FUNCTION |-------------------------------------------------------------------------------------------------------|
def header_base64_login(username: str, password: str) -> str:
    encode_pass: bytes = f"{username}:{password}".encode()
    return f"Basic {base64.b64encode(encode_pass).decode()}"


def header_base64_register(username: str, password: str, email: str) -> str:
    encode_register: bytes = f"{username}:{password}:{email}".encode()
    return f"Basic {base64.b64encode(encode_register).decode()}"


def token_return(username: str, password: str) -> str:
    header: dict[str] = {"Authorization": header_base64_login(username, password)}
    return json.loads(requests.post(f"{root_route}{login_route}", headers=header).text)['token']
# |--------------------------------------------------------------------------------------------------------------------|