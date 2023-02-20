# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                  API.auth.login.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from API.secure.base.decrypt_base64 import Decrypt
from API.models.routes.auth.functions import Model
from API.json.auth.login import send_token_after_login
from API.status import *
# |--------------------------------------------------------------------------------------------------------------------|


def exec_login(credentials: str) -> tuple[dict[str], int]:
    # + Decryption +
    credentials: tuple[list[str] | dict[str], int] = Decrypt.Base64.read_authentication(credentials, "login")
    
    if credentials[1] != HTTP_200_OK:       # Compare status_code
        return credentials
    
    credentials: dict[str] = {"username": credentials[0][0], "password": credentials[0][1]}
    
    # + Model validation +
    validation: tuple[dict[str], int] = Model().login(credentials['username'], credentials['password'])
    if validation[1] != HTTP_202_ACCEPTED:
        return validation
    
    return send_token_after_login(credentials['username'])
    