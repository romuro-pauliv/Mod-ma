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


def name_validation(name: str) -> tuple[str, int]:
    if len(name) >= 4:
        # Ponctuation test |-------------------------------------------------------------------------------------------|
        for _char in name:
            if _char in "!\"#$%&'()*+,./:;<=>?@[\]^`{|}~ \t\n\r\x0b\x0c":
                return str("CHARACTER [" + _char +  "] NOT ALLOWED"), HTTP_400_BAD_REQUEST
        # |------------------------------------------------------------------------------------------------------------|
    else:
        return "THE INFORMED NAME MUST BE MORE THAN 4 CHARACTERS", HTTP_400_BAD_REQUEST
    return "VALID NAME", HTTP_202_ACCEPTED

def request_json(fields: list[str]) -> tuple[str, int]:
    for i in fields:
        try:
            if request.json[i]:
                pass
        except KeyError:
            return "BAD REQUEST", HTTP_400_BAD_REQUEST
    return "VALID FIELD", HTTP_202_ACCEPTED

class Model(object):
    @staticmethod
    def create_database(func: Callable[..., Any]) -> None:
        def wrapper(*args, **kwargs) -> Callable[..., tuple[str, int]]:
            # json validation |------------------------------------------------------------------------------------|
            valid_json = request_json(["database"])
            if valid_json[1] != HTTP_202_ACCEPTED:
                return valid_json
                
            valid_name = name_validation(request.json["database"])
            if valid_name[1] != HTTP_202_ACCEPTED:
                return valid_name
            # |----------------------------------------------------------------------------------------------------|
            
            return func(*args, **kwargs)
        
        wrapper.__name__ = func.__name__
        return wrapper