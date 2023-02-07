# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                              API.secure.pam.pam.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | imports |---------------------------------------------------------------------------------------------------------|
from API.db import get_db
from API.secure.token.IPT_token import IPToken

from API.models.tools.validations import Validate

from API.status import *

from flask import request

from typing import Any, Union
# |--------------------------------------------------------------------------------------------------------------------|

class PAM(object):
    def __init__(self, json: dict[str, Any]) -> None:
        # | json and username request |--------------------------------------------------------------------------------|
        self.json: dict[str, Any] = json
        self.username: str = IPToken.Tools.get_username_per_token(request.headers.get("Authorization"))
        # |------------------------------------------------------------------------------------------------------------|
        
        # | json model configuration |---------------------------------------------------------------------------------|
        self.required_fields: list[str] = ["user", "command", "method", "arguments"]
        self.command_value: list[str] = ["add", "remove"]
        self.method_value: list[str] = ["create", "read", "update", "delete"]
        # |------------------------------------------------------------------------------------------------------------|
    
    def get_privileges_fields(self) -> list[str]:
        remove_fields: list[str] = ["_id", "command", "datetime"]
        privileges: dict[str] = get_db().USERS.PRIVILEGES.find_one({"command": "privileges"})
        
        for rf in remove_fields:
            del privileges[rf]
        
        return privileges
    
    def json_validation(self) -> tuple[str, int]:
        # Verify if response is a json |-------------------------------------------------------------------------------|
        if not isinstance(self.json, dict):
            return "ONLY JSON ARE ALLOWED", HTTP_400_BAD_REQUEST
        # |------------------------------------------------------------------------------------------------------------|

        # Verify json fields |-----------------------------------------------------------------------------------------|
        for field in self.required_fields:
            try:
                if self.json[field]:
                    pass
            except KeyError:
                return "BAD REQUEST - KEY ERROR", HTTP_400_BAD_REQUEST
        return "JSON VALID", HTTP_202_ACCEPTED
    
    def user_validation(self) ->  Union[None, tuple[str, int]]:
        # Avoid NoSQL Injection |--------------------------------------------------------------------------------------|
        validate_str: tuple[str, int] = Validate.STRING.str_type(self.json["user"])
        if validate_str != HTTP_202_ACCEPTED:
            return validate_str
        
        validate_character: tuple[str, int] = Validate.STRING.character(self.json["user"])
        if validate_character[1] != HTTP_202_ACCEPTED:
            return validate_character
        # |------------------------------------------------------------------------------------------------------------|
        try:
            get_db().USERS.REGISTER.find_one({"username": self.json['user']})["username"]
        except TypeError:
            return f"USER [{self.json['user']}] NOT FOUND", HTTP_404_NOT_FOUND
        return "USER VALID", HTTP_202_ACCEPTED
    
    def command_validation(self) -> Union[None, tuple[str, int]]:
        # String validation |------------------------------------------------------------------------------------------|
        validate_str: tuple[str, int] = Validate.STRING.str_type(self.json["command"])
        if validate_str[1] != HTTP_202_ACCEPTED:
            return validate_str
        # |------------------------------------------------------------------------------------------------------------|
        if not self.json["command"] in self.command_value:
            return "COMMAND NOT VALID", HTTP_400_BAD_REQUEST
        return "COMMAND VALID", HTTP_202_ACCEPTED
    
    def method_validation(self) -> Union[None, tuple[str, int]]:
        # String validation |------------------------------------------------------------------------------------------|
        validate_str: tuple[str, int] = Validate.STRING.str_type(self.json["method"])
        if validate_str[1] != HTTP_202_ACCEPTED:
            return validate_str
        # |------------------------------------------------------------------------------------------------------------|
        if not self.json["method"] in self.method_value:
            return "CRUD METHOD NOT VALID", HTTP_400_BAD_REQUEST
        return "CRUD METHOD VALID", HTTP_202_ACCEPTED
    
    def arguments_validation(self) -> Union[None, tuple[str, int]]:
        # arguments list validation |----------------------------------------------------------------------------------|
        if not isinstance(self.json["arguments"], list):
            return "INVALID OBJECT TYPE IN ARGUMENTS", HTTP_400_BAD_REQUEST
        # |------------------------------------------------------------------------------------------------------------|
        
        # internal str | list arguments validation |-------------------------------------------------------------------|
        for arg_l in self.json["arguments"]:
            if not isinstance(arg_l, str) or isinstance(arg_l, list):
                return "INVALID OBJECT TYPE IN ARGUMENTS", HTTP_400_BAD_REQUEST
        # |------------------------------------------------------------------------------------------------------------|
        
        # str validation in privileges |-------------------------------------------------------------------------------|
        for arg_l in self.json['arguments']:
            if isinstance(arg_l, str):
                if not arg_l in ["database", "collection"]:
                    return f"INVALID PATH [{arg_l}]", HTTP_400_BAD_REQUEST
            
            if isinstance(arg_l, list):
                if len(arg_l) > 2:
                    return f"INVALID PATH - THE LIST MUST HAVE ONLY 2 ARGUMENTS [{str(arg_l)}]", HTTP_400_BAD_REQUEST
                
                
        # |------------------------------------------------------------------------------------------------------------|