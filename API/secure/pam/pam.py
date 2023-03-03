# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                              API.secure.pam.pam.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | imports |---------------------------------------------------------------------------------------------------------|
from API.db import get_db
from API.secure.token.IPT_token import IPToken
from API.json.responses.pam.pam_status import Responses
from API.models.tools.validations import Validate
from API.status import *

from flask import request

from typing import Any, Union, Callable
# |--------------------------------------------------------------------------------------------------------------------|

class PAM(object):
    def __init__(self, json: dict[str, Any]) -> None:
        # | json and username request |--------------------------------------------------------------------------------|
        self.json: dict[str, Any] = json
        self.username: str = IPToken.Tools.get_username_per_token(request.headers.get("Authorization"))
        self.authorized_user: list[str] = get_db().USERS.PRIVILEGES.find_one({"command": "pam"})['pam_users']
        # |------------------------------------------------------------------------------------------------------------|
        
        # | json model configuration |---------------------------------------------------------------------------------|
        self.required_fields: list[str] = ["user", "command", "method", "arguments"]
        self.command_value: list[str] = ["append", "remove"]
        self.method_value: list[str] = ["create", "read", "update", "delete"]
        # |------------------------------------------------------------------------------------------------------------|
    
    def get_privileges(self) -> list[str]:
        remove_fields: list[str] = ["_id", "command", "datetime"]
        privileges: dict[str] = get_db().USERS.PRIVILEGES.find_one({"command": "privileges"})
        
        for rf in remove_fields:
            del privileges[rf]
        
        return privileges
    
    def json_validation(self) -> tuple[str, int]:
        # Verify if response is a json |-------------------------------------------------------------------------------|
        if not isinstance(self.json, dict):
            return Responses.R4XX.only_json()
        # |------------------------------------------------------------------------------------------------------------|

        # Verify json fields |-----------------------------------------------------------------------------------------|
        for field in self.required_fields:
            try:
                if self.json[field]:
                    pass
            except KeyError:
                return Responses.R4XX.key_error()
        return Responses.R2XX.json_valid()
    
    def user_validation(self) -> tuple[str, int]:
        # Avoid NoSQL Injection |--------------------------------------------------------------------------------------|
        validate_str: tuple[str, int] = Validate.STRING.str_type(self.json["user"])
        if validate_str[1] != HTTP_202_ACCEPTED:
            return validate_str
        
        validate_character: tuple[str, int] = Validate.STRING.character(self.json["user"])
        if validate_character[1] != HTTP_202_ACCEPTED:
            return validate_character
        # |------------------------------------------------------------------------------------------------------------|
        if get_db().USERS.REGISTER.find_one({"username": self.json['user']}) is None:
            return Responses.R4XX.user_not_found(self.json["user"])
        
        return Responses.R2XX.user_valid()
    
    def command_validation(self) -> tuple[str, int]:
        # String validation |------------------------------------------------------------------------------------------|
        validate_str: tuple[str, int] = Validate.STRING.str_type(self.json["command"])
        if validate_str[1] != HTTP_202_ACCEPTED:
            return validate_str
        # |------------------------------------------------------------------------------------------------------------|
        if not self.json["command"] in self.command_value:
            return Responses.R4XX.invalid_command(self.json["command"])
        return Responses.R2XX.command_valid()
    
    def method_validation(self) -> tuple[str, int]:
        # String validation |------------------------------------------------------------------------------------------|
        validate_str: tuple[str, int] = Validate.STRING.str_type(self.json["method"])
        if validate_str[1] != HTTP_202_ACCEPTED:
            return validate_str
        # |------------------------------------------------------------------------------------------------------------|
        if not self.json["method"] in self.method_value:
            return Responses.R4XX.invalid_crud_method(self.json["method"])
        return Responses.R2XX.crud_method_valid()
    
    def arguments_validation(self) -> tuple[str, int]:
        # arguments list validation |----------------------------------------------------------------------------------|
        if not isinstance(self.json["arguments"], list):
            return Responses.R4XX.invalid_object_type_arguments()
        # |------------------------------------------------------------------------------------------------------------|
        
        # internal str | list arguments validation |-------------------------------------------------------------------|
        for arg_l in self.json["arguments"]:
            if not isinstance(arg_l, str):
                if not isinstance(arg_l, list):
                    return Responses.R4XX.invalid_item_in_arguments(arg_l)
        # |------------------------------------------------------------------------------------------------------------|
        
        # str validation in privileges |-------------------------------------------------------------------------------|
        for arg_l in self.json['arguments']:
            if isinstance(arg_l, str):
                if not arg_l in ["database", "collection"]:
                    return Responses.R4XX.invalid_path(arg_l)
            
            if isinstance(arg_l, list):
                if len(arg_l) > 2 or len(arg_l) < 2:
                    return Responses.R4XX.invalid_path_error_len_list(arg_l)
                
                for db_coll in arg_l:
                    if not isinstance(db_coll, str):
                        return Responses.R4XX.invalid_item_in_list(db_coll)
                
                # Extracting the privileges and configuring |----------------------------------------------------------|
                privileges: dict[str, dict] = self.get_privileges()
                del privileges['database'], privileges['collection']
                # |----------------------------------------------------------------------------------------------------|
                
                # Check the database values in privileges |------------------------------------------------------------|
                database_names: list[str] = [db_name for db_name in privileges.keys()]
                if not arg_l[0] in database_names:
                    return Responses.R4XX.database_not_found(arg_l[0])
                # |----------------------------------------------------------------------------------------------------|
                
                # Check the collection values in privileges |----------------------------------------------------------|
                collection_names: list[str] = [coll_name for coll_name in privileges[arg_l[0]].keys()]
                if not arg_l[1] in collection_names:
                    return Responses.R4XX.collection_not_found(arg_l[1])
                # |----------------------------------------------------------------------------------------------------|
        return Responses.R2XX.arguments_valid()
    
    def exec_validation(self) -> tuple[Union[str, dict[str, Union[str, list]]], int]:
        # Func validation list |---------------------------------------------------------------------------------------|
        func_validation_list: list[Callable[..., tuple[str, int]]] = [
            self.json_validation,
            self.user_validation,
            self.command_validation,
            self.method_validation,
            self.arguments_validation
        ]
        # |------------------------------------------------------------------------------------------------------------|
        
        # Itering the func_validation_list |---------------------------------------------------------------------------|
        for func_validation in func_validation_list:
            validation_response: tuple[str, int] = func_validation()
            if validation_response[1] != HTTP_202_ACCEPTED:
                return validation_response
        # |------------------------------------------------------------------------------------------------------------|
        
        return self.json, HTTP_202_ACCEPTED
    
    def update(self) -> tuple[str, int]:
        # Execute all validation |-------------------------------------------------------------------------------------|
        all_validation: tuple[Union[str, dict[str, Union[str, list]]], int] = self.exec_validation()
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