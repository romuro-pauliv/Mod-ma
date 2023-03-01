# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                               API.auth.register.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from API.json.responses.auth.delete_account_status import Responses
from API.models.routes.auth.functions import Model
from API.secure.base.decrypt_base64 import Decrypt
from API.db import get_db
from API.status import *
# |--------------------------------------------------------------------------------------------------------------------|

def exec_delete_account(credentials: str) -> tuple[dict[str], int]:
    # + decryption +
    credentials: tuple[dict[str], int | list[str], int] = Decrypt.Base64.read_authentication(credentials, "register")    
    if credentials[1] != HTTP_200_OK:
        return credentials
    
    credentials: dict[str] = {
        "username": credentials[0][0], "password": credentials[0][1], "email": credentials[0][2]
    }
    
    validation: tuple[dict[str], int] = Model().delete_account(
        credentials['username'], credentials['password'], credentials['email']
    )
    if validation[1] != HTTP_202_ACCEPTED:
        return validation
    
    # Delete Username of database |------------------------------------------------------------------------------------|
    get_db().USERS.REGISTER.delete_one({"username": credentials['username']})
    # |----------------------------------------------------------------------------------------------------------------|
    
    privileges: dict[str, list[str] | dict[str]] = get_db().USERS.PRIVILEGES.find_one({"command": "privileges"})
    # + Treatment of privileges +
    for key in ["_id", "command", "datetime"]:
        del privileges[key]
    
    # + delete username of privileges +    
    for master_keys in privileges.keys():
        update_operations: dict[str] = {}
        
        secondary_keys: list[str] = [i for i in privileges[master_keys].keys()]
        if secondary_keys == ["create", "read", "update", "delete"]:
            update_operations["$pull"] = {f"{master_keys}.create": credentials["username"],
                                          f"{master_keys}.read": credentials["username"],
                                          f"{master_keys}.update": credentials["username"],
                                          f"{master_keys}.delete": credentials["username"]
                                          }
            get_db().USERS.PRIVILEGES.update_one({"command": "privileges"}, update_operations)
        else:
            for secondary_key in privileges[master_keys].keys():
                methods: list[str] = [i for i in privileges[master_keys][secondary_key].keys()]
                if methods == ["create", "read", "update", "delete"]:
                    update_operations["$pull"] = {f"{master_keys}.{secondary_key}.create": credentials["username"],
                                                  f"{master_keys}.{secondary_key}.read": credentials["username"],
                                                  f"{master_keys}.{secondary_key}.update": credentials["username"],
                                                  f"{master_keys}.{secondary_key}.delete": credentials["username"],
                                                  }
                    get_db().USERS.PRIVILEGES.update_one({"command": "privileges"}, update_operations)
    
    return Responses.R2XX.correct_credentials()