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
    credentials_decrypt: list[str] = Decrypt.Base64.read_authentication(
        credentials, "login"
    )
    
    if credentials_decrypt[1] == HTTP_400_BAD_REQUEST:
        return credentials_decrypt
    
    # + Model validation +
    validation: tuple[dict[str], int] = Model().login(
        credentials_decrypt[0], credentials_decrypt[1]
    )
    if validation[1] != HTTP_202_ACCEPTED:
        return validation
    
    return send_token_after_login(credentials_decrypt[0])
    