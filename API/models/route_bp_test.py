# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                        API.models.route_db_test.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# imports |------------------------------------------------------------------------------------------------------------|
from API.status import *

from flask import request
from typing import Callable, Any
# |--------------------------------------------------------------------------------------------------------------------|


def string_validation(name: str) -> tuple[str, int]:
    if not isinstance(name, str):
        return "ONLY STRING ARE ALLOWED", HTTP_400_BAD_REQUEST

    if len(name) >= 4:
        # Ponctuation test |-------------------------------------------------------------------------------------------|
        for _char in name:
            if _char in "!\"#$%&'()*+,./:;<=>?@[\]^`{|}~ \t\n\r\x0b\x0c":
                return str("CHARACTER [" + _char +  "] NOT ALLOWED"), HTTP_400_BAD_REQUEST
        # |------------------------------------------------------------------------------------------------------------|
    else:
        return "THE INFORMED NAME MUST BE MORE THAN 4 CHARACTERS", HTTP_400_BAD_REQUEST
    return "VALID NAME", HTTP_202_ACCEPTED

def json_fields_validation(fields: list[str]) -> tuple[str, int]:
    for i in fields:
        try:
            if request.json[i]:
                pass
        except KeyError:
            return "BAD REQUEST", HTTP_400_BAD_REQUEST
    return "VALID FIELD", HTTP_202_ACCEPTED

class Model(object):
    @staticmethod
    def create_database(func: Callable[..., Any]) -> Callable[..., Callable[..., tuple[str, int]]]:
        def wrapper(*args, **kwargs) -> Callable[..., tuple[str, int]]:

            # json validation |------------------------------------------------------------------------------------|
            valid_json = json_fields_validation(["database"])
            if valid_json[1] != HTTP_202_ACCEPTED:
                return valid_json
                
            valid_name = string_validation(request.json["database"])
            if valid_name[1] != HTTP_202_ACCEPTED:
                return valid_name
            # |----------------------------------------------------------------------------------------------------|
            
            return func(*args, **kwargs)
        
        wrapper.__name__ = func.__name__
        return wrapper
    
    @staticmethod
    def create_collection(func: Callable[..., Any]) -> Callable[..., Callable[..., tuple[str, int]]]:
        def wrapper(*args, **kwargs) -> Callable[..., tuple[str, int]]:
            
            fields: list[str] = ["database", "collection"]

            # json validation |----------------------------------------------------------------------------------------|
            valid_json = json_fields_validation(fields)
            if valid_json[1] != HTTP_202_ACCEPTED:
                return valid_json
            
            for field in fields:
                valid_name = string_validation(request.json[field])
                if valid_name[1] != HTTP_202_ACCEPTED:
                    return valid_name
            # |--------------------------------------------------------------------------------------------------------|

            return func(*args, **kwargs)
        
        wrapper.__name__ = func.__name__
        return wrapper
