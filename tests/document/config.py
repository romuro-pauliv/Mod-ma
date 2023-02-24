# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                 database.config.py |
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

database: str = "/database/"
collection: str = '/collection/'
document: str = "/document/"
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


def get_id(filter: dict[str], database: str, collection: str) -> str:
    _id_doc_iterable: str = mongo[database][collection].find(filter)
    _id_doc: str = ""
    for doc in _id_doc_iterable:
        _id_doc: str = doc['_id']
    return _id_doc
# |--------------------------------------------------------------------------------------------------------------------|