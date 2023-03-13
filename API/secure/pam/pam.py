# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                              API.secure.pam.pam.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | imports |----------------------------------------------------------------------------------------------------------|
from API.db import get_db
from API.secure.token.IPT_token import IPToken
from API.json.responses.pam.pam_status import Responses
from API.secure.pam.validation.exec import execute_validation
from API.status import *

from flask import request

from typing import Any, Union
# |--------------------------------------------------------------------------------------------------------------------|

class PAM(object):
    def __init__(self, json: dict[str, Any]) -> None:
        # | json and username request |--------------------------------------------------------------------------------|
        self.json: dict[str, Any] = json
        self.username: str = IPToken.Tools.get_username_per_token(request.headers.get("Authorization"))
        self.authorized_user: list[str] = get_db().USERS.PRIVILEGES.find_one({"command": "pam"})['pam_users']
        # |------------------------------------------------------------------------------------------------------------|

    def update(self) -> tuple[str, int]:
        # Execute all validation |-------------------------------------------------------------------------------------|
        all_validation: tuple[Union[str, dict[str, Union[str, list]]], int] = execute_validation(self.json)
        if all_validation[1] != HTTP_202_ACCEPTED:
            return all_validation
        # |------------------------------------------------------------------------------------------------------------|
        
        # Only "admin" have access to PAM |----------------------------------------------------------------------------|
        if not self.username in self.authorized_user:
            return Responses.R4XX.unauthorized_request(self.username)
        # |------------------------------------------------------------------------------------------------------------|
        
        # Get privileges |---------------------------------------------------------------------------------------------|
        privileges: dict[str, dict] = get_db().USERS.PRIVILEGES.find_one({"command": "privileges"})
        # |------------------------------------------------------------------------------------------------------------|
        
        # Execute update privileges |----------------------------------------------------------------------------------|
        for args in self.json["arguments"]:
            # | To database, collection (str) |------------------------------------------------------------------------|
            if isinstance(args, str):
                # Append command |-------------------------------------------------------------------------------------|
                if self.json['command'] == "append":
                    if self.json['user'] not in privileges[args][self.json['method']]:
                        if self.username in privileges[args][self.json['method']]:
                            privileges[args][self.json['method']].append(self.json['user'])
                        else:
                            return Responses.R4XX.unauthorized_modification(
                                self.username, args, None, self.json['method'])
                # |----------------------------------------------------------------------------------------------------|
                
                # Remove command |-------------------------------------------------------------------------------------|
                elif self.json['command'] == "remove":
                    if self.json['user'] in privileges[args][self.json['method']]:
                        if self.username in privileges[args][self.json['method']]:
                            privileges[args][self.json['method']].remove(self.json['user'])
                        else:
                            return Responses.R4XX.unauthorized_modification(
                                self.username, args, None, self.json['method'])
                # |----------------------------------------------------------------------------------------------------|
            if isinstance(args, list):
                # Append command |-------------------------------------------------------------------------------------|
                if self.json["command"] == "append":
                    if self.json["user"] not in privileges[args[0]][args[1]][self.json["method"]]:
                        if self.username in privileges[args[0]][args[1]][self.json["method"]]:
                            privileges[args[0]][args[1]][self.json["method"]].append(self.json['user'])
                        else:
                            return Responses.R4XX.unauthorized_modification(
                                self.username, args[0], args[1], self.json["method"])
                # |----------------------------------------------------------------------------------------------------|
                
                # Remove command |-------------------------------------------------------------------------------------|
                if self.json["command"] == "remove":
                    if self.json["user"] in privileges[args[0]][args[1]][self.json["method"]]:
                        if self.username in privileges[args[0]][args[1]][self.json["method"]]:
                            privileges[args[0]][args[1]][self.json["method"]].remove(self.json["user"])
                        else:
                            Responses.R4XX.unauthorized_modification(
                                self.username, args[0], args[1], self.json["method"])
                # |----------------------------------------------------------------------------------------------------|
                
        # Update |-----------------------------------------------------------------------------------------------------|
        del privileges["_id"]
        get_db().USERS.PRIVILEGES.delete_one({"command": "privileges"})
        get_db().USERS.PRIVILEGES.insert_one(privileges)
        
        return Responses.R2XX.update_privileges()