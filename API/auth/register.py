# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                               API.auth.register.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from API.json.responses.auth.register_status import Responses
from API.models.routes.auth.functions import Model
from API.secure.base.decrypt_base64 import Decrypt
from API.json.auth.register import new_user
from API.db import get_db
from API.status import *
# |--------------------------------------------------------------------------------------------------------------------|

def exec_register(credentials: str) -> tuple[dict[str], int]:
    # + Decryption +
    credentials_decrypt: list[str] = Decrypt.Base64.read_authentication(
        credentials, "register"
    )
    if credentials_decrypt[1] == HTTP_400_BAD_REQUEST:
        return credentials_decrypt
    
    # + Model validation +
    validation: tuple[dict[str], int] = Model().register(
        credentials_decrypt[0], credentials_decrypt[1], credentials_decrypt[2]
    )
    if validation[1] != HTTP_202_ACCEPTED:
        return validation
    
    # + register in database +
    get_db().USERS.REGISTER.insert_one(new_user(
        credentials_decrypt[0], credentials_decrypt[1], credentials_decrypt[2]
    ))
    return Responses.ExecRegister.R2XX.successfully_registered()