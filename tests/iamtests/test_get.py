# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                     test.iam.require_privileges.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
import requests
from config import *
from typing import Any
# |--------------------------------------------------------------------------------------------------------------------|

# | Parameters |-------------------------------------------------------------------------------------------------------|
credentials: dict[str] = {"username": "iamtest", "password": "123!IamTest", "email": "iamtest@iamtest.com"}
register_base64: str = header_base64_register(credentials['username'], credentials['password'], credentials['email'])
requests.post(f"{root_route}{register_route}", headers={"Register": register_base64})
header: dict[str] = {"Authorization": f"Bearer {token_login(credentials['username'], credentials['password'])}"}
# |--------------------------------------------------------------------------------------------------------------------|

# | Functions |--------------------------------------------------------------------------------------------------------|
def response_assert(hypothetical_response: str, request_obj: requests.models.Response) -> bool:
    return (hypothetical_response == json.loads(request_obj.text)['response'])

def status_code_assert(hypothetical_status_code: int, request_obj: requests.models.Response) -> bool:
    return (hypothetical_status_code == request_obj.status_code)
# |--------------------------------------------------------------------------------------------------------------------|

