# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                    test.pam.test_funcionalities.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
import requests
from config import *
from typing import Any
# |--------------------------------------------------------------------------------------------------------------------|

# | FUNCTIONS |--------------------------------------------------------------------------------------------------------|
def PAM_function(header: dict[str], send_json: dict[str, str | list[str]]) -> requests.models.Response:
    return requests.put(f"{root_route}{iam_route}", headers=header, json=send_json)
# |--------------------------------------------------------------------------------------------------------------------|


# | Admin credentials |------------------------------------------------------------------------------------------------|
cred_admin: dict[str] = {"username": "admin", "password": "123!Admin"}
admin_header: dict[str] = {"Authorization": f"Basic {token_login(cred_admin['username'], cred_admin['password'])}"}
# |--------------------------------------------------------------------------------------------------------------------|


# | Pamtest credentials |----------------------------------------------------------------------------------------------|
cred_pamtest: dict[str] = {"username": "pamtest", "password": "123!PamTest", "email": "pamtest@pamtest.com"}

def test_pamtest_register() -> None:
    response: requests.models.Response = requests.post(
        f"{root_route}{register_route}", headers={
            "Register": header_base64_register(
                username=cred_pamtest["username"],
                password=cred_pamtest["password"],
                email=cred_pamtest["email"]
            )
        }
    )
    
    if response.status_code == 201:
        assert response.status_code == 201
    else:
        assert response.status_code == 403
# |--------------------------------------------------------------------------------------------------------------------|

# | RESET USER |-------------------------------------------------------------------------------------------------------|
def test_reset_pamtest() -> None:
    header: dict[str] = {
        "Authorization":f"Basic {token_login(cred_pamtest['username'], cred_pamtest['password'])}",
        "Register": header_base64_register(
            username=cred_pamtest['username'],
            password=cred_pamtest['password'],
            email=cred_pamtest['email']
        )
    }
    
    response: requests.models.Response = requests.delete(f"{root_route}{register_route}", headers=header)
    assert response.status_code == 202
# |--------------------------------------------------------------------------------------------------------------------|