# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                     API.iam.add.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from typing import Callable, Any
from functools import wraps
from flask import request

from API.secure.token.IPT_token import IPToken
from API.status import *
from API.db import get_db
# |--------------------------------------------------------------------------------------------------------------------|


class IAM(object):
    class Add(object):
        def __init__(self, PAM: str) -> None:
            self.PAM: str = PAM
            self.username: str = IPToken.Tools.get_username_per_token(request.headers.get("Authorization"))
            self.privileges: dict[list | dict] = get_db().USERS.PRIVILEGES.find_one({"command": "privileges"})
            
            self.input_username_privileges: list[str] = []
            if self.PAM == self.username:
                self.input_username_privileges: list[str] = [self.PAM]
            else:
                self.input_username_privileges: list[str] = [self.PAM, self.username]
            
            self.PAM_method: dict[str, list[str]] = {
                "create": [self.PAM], "read": [self.PAM], "update": [self.PAM], "delete": [self.PAM]
            }
            
            self.IAM_method: dict[str, list[str]] = {
                "create": self.input_username_privileges, "read": self.input_username_privileges,
                "update": self.input_username_privileges, "delete": self.input_username_privileges
            }
            
        def new_database(self, func: Callable[..., Any]) -> Callable[..., tuple[dict[str, Any], int]]:
            @wraps(func)
            def wrapper(*args, **kwargs) -> tuple[dict[str, Any], int]:
                # + Execute function +
                val: tuple[dict[str, Any], int] = func(*args, **kwargs)
                
                if val[1] == HTTP_202_ACCEPTED:
                    database_name: str = request.json['database'].lower()
                    self.privileges[database_name]: dict[str, dict[str]] = {}
                    
                    for collection_name in get_db()[database_name].list_collection_names():
                        if collection_name == "LOG":
                            self.privileges[database_name][collection_name]: dict[str, list[str]] = self.PAM_method
                        else:
                            self.privileges[database_name][collection_name]: dict[str, list[str]] = self.IAM_method
                    
                    get_db().USERS.PRIVILEGES.delete_one({"command": "privileges"})
                    del self.privileges['_id']
                    get_db().USERS.PRIVILEGES.insert_one(self.privileges)

                return val
            return wrapper