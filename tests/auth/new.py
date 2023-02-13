import requests
from config import *
from typing import Any

credentials: dict[str] = {
    "username": "admin",
    "password": "123!Admin"
}

header_token_config: dict[str] = {
    "field": "Authorization",
    "prefix": "Token "
}

def func_request(header: dict[str] | Any) -> requests:
    response: requests = requests.post(f"{root_route}{test_token_route}", headers=header)
    return response


def test_real_token() -> None:
    response: requests = func_request()
