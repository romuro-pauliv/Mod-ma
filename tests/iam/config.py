# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                     test.config.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | imports |----------------------------------------------------------------------------------------------------------|
import os
import json
import base64
import requests

from pymongo import MongoClient
from pathlib import Path
from dotenv import load_dotenv
# |--------------------------------------------------------------------------------------------------------------------|

# ROUTES |=============================================================================================================|
root_route: str = "http://127.0.0.1:5000"
login_route: str = "/auth/login"
register_route: str = "/auth/register"

create_database_route: str = "/tests/test-create-database"
create_collection_route: str = "/tests/test-create-collection"
create_document_route: str = "/tests/test-create-document"

read_database_route: str = "/tests/test-read-database"
read_collection_route: str = '/tests/test-read-collection'
read_documents_route: str = '/tests/test-read-document'
# |====================================================================================================================|

# MONGO CLIENT |=======================================================================================================|
json_path: str = Path("tests/path.json")
with open(json_path, 'r') as js_file:
    json_dt: dict[str] = json.load(js_file)
    js_file.close()
load_dotenv(dotenv_path=Path(json_dt['dotenv']))

mongo = MongoClient(os.getenv('MONGO_URI'))
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