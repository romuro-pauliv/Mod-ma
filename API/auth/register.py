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
    credentials: tuple[dict[str] | list[str], int] = Decrypt.Base64.read_authentication(credentials, "register")
    
    if credentials[1] != HTTP_200_OK:       # Compare status_code
        return credentials
    
    credentials: dict[str] = {
        "username": credentials[0][0], "password": credentials[0][1], "email": credentials[0][2]
    }
        
    # + Model validation +
    validation: tuple[dict[str], int] = Model().register(
        credentials['username'], credentials["password"], credentials["email"]
    )
    if validation[1] != HTTP_202_ACCEPTED:
        return validation
    
    # + register in database +
    get_db().USERS.REGISTER.insert_one(new_user(
        credentials["username"], credentials["password"], credentials["email"]
    ))
    return Responses.ExecRegister.R2XX.successfully_registered()