# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                         API.iam.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | imports |----------------------------------------------------------------------------------------------------------|
from .db import get_db
from .secure.token.IPT_token import IPToken
from .status import *

from typing import Callable, Any

from pymongo import cursor
from flask import request
from functools import wraps

import datetime
# |--------------------------------------------------------------------------------------------------------------------|

class Privileges(object):
    def __init__(self, PAM: str) -> None:
        self.pam = PAM
        self.mongo = get_db
        self.methods: dict[str, list[str]] = {
            "create": [PAM],
            "read": [PAM],
            "update": [PAM],
            "delete": [PAM]
        }
        self.config_names: list[str] = [
            "_id", "command", "datetime",
            "database", "collection", "documents",
            "admin", "local"
            ]
    
    def get_keys(self, data: dict[str]) -> list[str]:
        keys: list[str] = []
        for d in data.keys():
            keys.append(d)
        return keys
    
    def update(self) -> None:
        # GET PRIVILEGES JSON |========================================================================================|
        for dt in self.mongo().USERS.PRIVILEGES.find({"command": "privileges"}):
            real_privileges: dict = dt        
        # |============================================================================================================|

        mongo_db_list: list[str] = self.mongo().list_database_names()

        # GET NEW DB |=================================================================================================|
        # REGISTERED DB |----------------------------------------------------------------------------------------------|
        registered_db: list[str] = self.get_keys(real_privileges)
        # |------------------------------------------------------------------------------------------------------------|
        
        for db in mongo_db_list:                                          # Iteration of the list from the existing db
            if db not in ["admin", "local"]:                              # Does not perform any acition for the dbs
                
                # UPDATE DATABASE ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                if db not in registered_db:                               # Compares registered db with existing ones
                    real_privileges[db]: dict[str, dict] = {}             # Register the new db
                # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                    
                for coll in self.mongo()[db].list_collection_names():     # Iteration of the list from the existing coll
                        
                    # REGISTERED COLLECTIONS |-------------------------------------------------------------------------|
                    registered_coll: list[str] = self.get_keys(real_privileges[db])
                    # |------------------------------------------------------------------------------------------------|

                    # UPDATE COLLECTION ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                    if coll not in registered_coll:                       # Compares registered coll with existing ones
                        real_privileges[db][coll] = self.methods          # Register the new coll
                    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # |============================================================================================================|

        # DELETE NON-EXISTENT DB |=====================================================================================|
        registered_db: list[str] = [elem for elem in self.get_keys(real_privileges) if elem not in self.config_names]

        for db in registered_db:
            # UPDATE DATABSE +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            if db not in mongo_db_list:                                      # Compares real db with registered
                del real_privileges[db]                                      # Register the delete db
            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            
            if db in mongo_db_list:
                registered_coll: list[str] = self.get_keys(real_privileges[db])
                for coll in registered_coll:
                    if coll not in self.mongo()[db].list_collection_names():   # Compares real coll with registered
                        del real_privileges[db][coll]                        # Register the delete coll
        # |============================================================================================================|

        # DELETE OLDERS PRIVILEGES |===================================================================================|
        self.mongo().USERS.PRIVILEGES.delete_one({"command": "privileges"})
        # |============================================================================================================|

        # Insert in database |=========================================================================================|
        del real_privileges['_id']
        self.mongo().USERS.PRIVILEGES.insert_one(real_privileges)

    class Add(object):
        def __init__(self) -> None:
            self.privileges = Privileges("admin")
        
        def database(self, func: Callable[..., Any]) -> Callable:
            @wraps(func)
            def involved(*args, **kwargs) -> Callable[..., Any]:
                val: tuple[str, int] = func(*args, **kwargs)

                if val[1] == HTTP_201_CREATED:
                    # GET PRIVILEGES JSON |============================================================================|
                    for dt in self.privileges.mongo().USERS.PRIVILEGES.find({"command": "privileges"}):
                        real_privileges: dict = dt
                    # |================================================================================================|

                    username: str = IPToken.Tools.get_username_per_token(request.headers.get("Authorization"))
                    
                    # STRUCTURE OF ARRAY PRIVILEGES USERNAME |=========================================================|
                    if username == self.privileges.pam:
                        input_usernames_privileges: list[str] = [username]
                    else:
                        input_usernames_privileges: list[str] = [self.privileges.pam, username]
                    # |================================================================================================|

                    db_name: str = request.json["database"]
                        
                    # STRUCTURE OF UPDATE |============================================================================|
                    real_privileges[db_name]: dict[str, dict[str]] = {}
                    for coll in self.privileges.mongo()[db_name].list_collection_names():
                        if coll == "LOG":
                            real_privileges[db_name][coll]: dict[str, list[str]] = self.privileges.methods
                        else:
                            real_privileges[db_name][coll]: dict[str, list[str]] = {
                                "create": input_usernames_privileges,
                                "read": input_usernames_privileges,
                                "update": input_usernames_privileges,
                                "delete": input_usernames_privileges
                            }
                    # |================================================================================================|
                        
                    # DELETE OLDERS PRIVILEGES |=======================================================================|
                    self.privileges.mongo().USERS.PRIVILEGES.delete_one({"command":"privileges"})
                    # |================================================================================================|

                    # Insert in privileges |===========================================================================|
                    del real_privileges['_id']
                    self.privileges.mongo().USERS.PRIVILEGES.insert_one(real_privileges)

                return val
            involved.__name__ == func.__name__
            return involved

        def collection(self, func: Callable[..., Any]) -> Callable:
            @wraps(func)
            def involved(*args, **kwargs) -> Callable[..., Any]:
                val: tuple[str, int] = func(*args, **kwargs)

                if val[1] == HTTP_201_CREATED:
                    # GET PRIVILEGES JSON |============================================================================|
                    for dt in self.privileges.mongo().USERS.PRIVILEGES.find({"command": "privileges"}):
                        real_privileges: dict = dt
                    # |================================================================================================|

                    username: str = IPToken.Tools.get_username_per_token(request.headers.get("Authorization"))

                    # STRUCTURE OF ARRAY PRIVILEGES USERNAME |=========================================================|
                    if username == self.privileges.pam:
                        input_usernames_privileges: list[str] = [username]
                    else:
                        input_usernames_privileges: list[str] = [self.privileges.pam, username]
                    # |================================================================================================|

                    db_name: str = request.json['database']
                    cl_name: str = request.json['collection']

                    # STRUCTURE OF UPDATE |============================================================================|
                    real_privileges[db_name][cl_name]: dict[str, list[str]] = {
                        "create": input_usernames_privileges,
                        "read": input_usernames_privileges,
                        "update": input_usernames_privileges,
                        "delete": input_usernames_privileges
                    }
                    # |================================================================================================|

                    # DELETE OLDERS PRIVILEGES |=======================================================================|
                    self.privileges.mongo().USERS.PRIVILEGES.delete_one({"command": "privileges"})
                    # |================================================================================================|

                    # Insert in privileges |===========================================================================|
                    del real_privileges['_id']
                    self.privileges.mongo().USERS.PRIVILEGES.insert_one(real_privileges)
                return val
            involved.__name__ == func.__name__
            return involved

class IAM(object):
    @staticmethod
    def check_permission(method: str, structure: list | str) -> Callable:
        def inner(func: Callable[..., Any]) -> Callable:
            @wraps(func)
            def involved(*args, **kwargs) -> Callable[..., Any]:
                # GET USERNAME |---------------------------------------------------------------------------------------|
                username: str = IPToken.Tools.get_username_per_token(request.headers.get("Authorization"))
                # |----------------------------------------------------------------------------------------------------|

                # REQUEST THE PRIVILEGES DATA |------------------------------------------------------------------------|
                privileges: dict = get_db().USERS.PRIVILEGES.find_one({"command": "privileges"})
                # |----------------------------------------------------------------------------------------------------|

                # DATABASE, COLLECTION |-------------------------------------------------------------------------------|
                if structure in ["database", "collection"]:
                    if username in privileges[structure][method]:
                        return func(*args, **kwargs)
                    else:
                        return "REQUIRE PRIVILEGES", HTTP_403_FORBIDDEN
                # |----------------------------------------------------------------------------------------------------|
                # SPECIFIC COLLECTION |--------------------------------------------------------------------------------|
                elif structure == "especific":
                    rst_json: dict[str] = request.json
                    try:
                        if username in privileges[rst_json['database']][rst_json['collection']][method]:
                            return func(*args, **kwargs)
                        else:
                            return "REQUIRE PRIVILEGES", HTTP_403_FORBIDDEN
                    except KeyError:
                        return "BAD REQUEST - DATABASE OR COLLECTION NOT FOUND", HTTP_400_BAD_REQUEST
                # |----------------------------------------------------------------------------------------------------|
                else:
                    return "BAD REQUEST - STRUCTURE", HTTP_400_BAD_REQUEST            
            
            involved.__name__ == func.__name__
            return involved
        return inner