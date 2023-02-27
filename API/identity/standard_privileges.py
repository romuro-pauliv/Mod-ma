# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                     API.iam.standart_privileges.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | imports |----------------------------------------------------------------------------------------------------------|
from API.status import *
from API.secure.base.decrypt_base64 import Decrypt
from API.db import get_db

from typing import Callable, Any
from functools import wraps
from flask import request
# |--------------------------------------------------------------------------------------------------------------------|

class IAM(object):
    class StandardPrivileges(object):
        def __init__(self) -> None:
            self.privileges_query: dict[str] = {"command": "privileges"}
            self.standard_privileges_query: dict[str] = {"command": "standard privileges"}
            self.username: str
            self.privileges: dict[str, dict | list]
            self.standard_privileges: dict[str, dict | list]
            
        def add(self, func: Callable[..., Any]) -> Callable[..., tuple[dict[str], int]]:
            @wraps(func)
            def wrapper(*args, **kwargs) -> tuple[dict[str], int]:
                # + Execute function +
                val: tuple[dict[str], int] = func(*args, **kwargs)
                
                if val[1] == HTTP_201_CREATED:
                    
                    # + Get variables and IAM documents +
                    self.username: str = Decrypt.Base64.read_authentication(
                        header_credentials=request.headers.get("Register"), _method="register")[0][0]
                    self.privileges: dict[str, dict | list] = get_db().USERS.PRIVILEGES.find_one(self.privileges_query)
                    self.standard_privileges: dict[str, dict | list] = get_db().USERS.PRIVILEGES.find_one(
                        self.standard_privileges_query)
                    
                    
                    # + Standard Privileges treatment +
                    delete_keys: list[str] = ["_id", "command", "datetime"]
                    for keys in delete_keys:
                        del self.standard_privileges[keys]
                    
                    # Update Privileges with Standard Privileges
                    for master_method in [i for i in self.standard_privileges.keys()]:
                        # + Add privileges to database and collection methods +
                        if isinstance(self.standard_privileges[master_method], list):
                            for privileges_method in self.standard_privileges[master_method]:
                                if self.username not in self.privileges[master_method][privileges_method]:
                                    # + append username in standard privileges +
                                    self.privileges[master_method][privileges_method].append(self.username)
                        else:
                        # + Add privileges to specific databases and collections +
                            for collection_name in [i for i in self.standard_privileges[master_method].keys()]:
                                for privileges_method in self.standard_privileges[master_method][collection_name]:
                                    if self.username not in \
                                        self.privileges[master_method][collection_name][privileges_method]:
                                        # + append username in standard privileges +
                                        self.privileges[master_method][collection_name]\
                                            [privileges_method].append(self.username)
                    
                    # + update +
                    get_db().USERS.PRIVILEGES.delete_one(self.privileges_query)
                    del self.privileges["_id"]
                    get_db().USERS.PRIVILEGES.insert_one(self.privileges)
                    
                return val
            return wrapper