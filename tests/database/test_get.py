# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                          test.database.test_get.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | imports |----------------------------------------------------------------------------------------------------------|
import requests
from config import *
from typing import Any
# |--------------------------------------------------------------------------------------------------------------------|

# | Set data |---------------------------------------------------------------------------------------------------------|
credentials: dict[str] = {"username": "admin", "password": "123!Admin"}
header: dict[str] = {"Authorization": f"Bearer {token_return(credentials['username'], credentials['password'])}"}
# |--------------------------------------------------------------------------------------------------------------------|

# | function |---------------------------------------------------------------------------------------------------------|
def get_function(json_body: dict[str, Any]) -> requests.models.Response:
    return requests.get(f"{root_route}{database}", headers=header, json=json_body)

def response_assert(hypothetical_response: str, request_obj: requests.models.Response) -> bool:
    return (hypothetical_response == json.loads(request_obj.text)["response"])

def status_code_assert(hypothetical_status_code: str, request_obj: requests.models.Response) -> bool:
    return (hypothetical_status_code == request_obj.status_code)
# |--------------------------------------------------------------------------------------------------------------------|

# | Test Read Database |-----------------------------------------------------------------------------------------------|
def test_read_database() -> None:
    response: requests.models.Response = get_function(None)
    assert status_code_assert(200, response)
# |--------------------------------------------------------------------------------------------------------------------|

# | Test with wrong requests |-----------------------------------------------------------------------------------------|
def test_sended_json() -> None:
    response: requests.models.Response = get_function({"testing": "mode"})
    assert status_code_assert(200, response)
# |--------------------------------------------------------------------------------------------------------------------|