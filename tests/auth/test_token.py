# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                 test.test_token.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | imports |----------------------------------------------------------------------------------------------------------|
import requests
import time
import jwt
from werkzeug.security import generate_password_hash
import datetime
from config import *
from typing import Any
# |--------------------------------------------------------------------------------------------------------------------|

def test_real_token() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    # + request +
    rtn = requests.post(f"{root_route}{test_token_route}", headers=header)

    # + tests +
    assert rtn.text == "TEST OK"
    assert rtn.status_code == 202


def test_without_token() -> None:
    # + header +
    header: dict[None] = {}

    # + request +
    rtn = requests.post(f"{root_route}{test_token_route}", headers=header)

    # + tests +
    assert json.loads(rtn.text)["response"] == "A STRING WAS NOT IDENTIFIED IN THE TOKEN"
    assert rtn.status_code == 400


def test_expired_signature_token() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    # + request +
    time.sleep(25)
    rtn = requests.post(f"{root_route}{test_token_route}", headers=header)

    # + tests +
    assert json.loads(rtn.text)["response"] == "EXPIRED TOKEN"
    assert rtn.status_code == 403


def test_invalid_token() -> None:
    token: str = token_return("admin", "123!Admin")
    token: str = token + "a"
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    # + request +
    rtn = requests.post(f"{root_route}{test_token_route}", headers=header)

    # + tests +
    assert json.loads(rtn.text)["response"] == "INVALID TOKEN"
    assert rtn.status_code == 403


def test_wrong_formatting_token() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token WRONG {token}"}

    # + request +
    rtn = requests.post(f"{root_route}{test_token_route}", headers=header)

    # + tests +
    assert json.loads(rtn.text)["response"] == "INVALID TOKEN"
    assert rtn.status_code == 403


def test_false_ip_address_token() -> None:
    # + generate false token with false ip address +
    false_ip: str = "142.250.219.206"

    encode_dict_token: dict[str, str | datetime.datetime] = {
        "hash": generate_password_hash(false_ip),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=20)
    }

    token: str = jwt.encode(payload=encode_dict_token, key="dev", algorithm="HS256")
    
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    # + request +
    rtn = requests.post(f"{root_route}{test_token_route}", headers=header)

    # + tests +
    assert json.loads(rtn.text)["response"] == "IP ADDRESS DOES NOT MATCH"
    assert rtn.status_code == 403


def test_colon_error() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": token}

    # + request +
    rtn = requests.post(f"{root_route}{test_token_route}", headers=header)

    # + tests +
    assert json.loads(rtn.text)["response"] == "WAS NOT IDENTIFIED [:] COLON IN THE CREDENTIALS"
    assert rtn.status_code == 400
