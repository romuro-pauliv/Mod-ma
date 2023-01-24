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
from functools import wraps
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


def dictionary_validation(dictionary: dict[str, Any]) -> tuple[str, int]:
    if not isinstance(dictionary, dict):
        return "ONLY JSON ARE ALLOWED", HTTP_400_BAD_REQUEST
    
    for key in dictionary.keys():
        if len(key) < 4:
            return "THE INFORMED FIELD MUST BE MORE THAN 4 CHARACTERS", HTTP_400_BAD_REQUEST
    
    return "VALID DICT", HTTP_202_ACCEPTED


def json_fields_validation(fields: list[str]) -> tuple[str, int]:
    for i in fields:
        try:
            if request.json[i]:
                pass
        except KeyError:
            return "BAD REQUEST - KEY ERROR", HTTP_400_BAD_REQUEST
    return "VALID FIELD", HTTP_202_ACCEPTED


class Model(object):
    @staticmethod
    def create_database(func: Callable[..., Any]) -> Callable[..., Callable[..., tuple[str, int]]]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Callable[..., tuple[str, int]]:

            # json validation |----------------------------------------------------------------------------------------|
            valid_json = json_fields_validation(["database"])
            if valid_json[1] != HTTP_202_ACCEPTED:
                return valid_json
                
            valid_name = string_validation(request.json["database"])
            if valid_name[1] != HTTP_202_ACCEPTED:
                return valid_name
            # |--------------------------------------------------------------------------------------------------------|
            
            return func(*args, **kwargs)
        
        return wrapper
    
    @staticmethod
    def create_collection(func: Callable[..., Any]) -> Callable[..., Callable[..., tuple[str, int]]]:
        @wraps(func)
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
        
        return wrapper
    
    @staticmethod
    def create_document(func: Callable[..., Any]) -> Callable[..., Callable[..., tuple[str | dict, int]]]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Callable[..., tuple[str | dict, int]]:

            fields: list[str] = ["database", "collection", "document"]

            # json validation |----------------------------------------------------------------------------------------|
            valid_json = json_fields_validation(fields)
            if valid_json[1] != HTTP_202_ACCEPTED:
                return valid_json
            
            for field in fields[0:1]:
                valid_name = string_validation(request.json[field])
                if valid_name[1] != HTTP_202_ACCEPTED:
                    return valid_name
            # |--------------------------------------------------------------------------------------------------------|

            # dict validation |----------------------------------------------------------------------------------------|
            valid_dict: dict[str, Any] = dictionary_validation(request.json['document'])
            if valid_dict[1] != HTTP_202_ACCEPTED:
                return valid_dict
            # |--------------------------------------------------------------------------------------------------------|

            return func(*args, **kwargs)
        
        return wrapper
    
    @staticmethod
    def read_collection(func: Callable[..., Any]) -> Callable[..., Callable[..., tuple[list[str] | str, int]]]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Callable[..., tuple[list[str] | str, int]]:

            fields: list[str] = ["database"]

            # json validation |----------------------------------------------------------------------------------------|
            valid_json = json_fields_validation(fields)
            if valid_json[1] != HTTP_202_ACCEPTED:
                return valid_json
            # \--------------------------------------------------------------------------------------------------------|

            return func(*args, **kwargs)
        
        return wrapper
    
    @staticmethod
    def read_document(func: Callable[..., Any]) -> Callable[..., Callable[..., tuple[list[dict] | str, int]]]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Callable[..., tuple[list[dict] | str, int]]:

            fields: list[str] = ["database", "collection", "filter"]

            # json validation |----------------------------------------------------------------------------------------|
            valid_json = json_fields_validation(fields)
            if valid_json[1] != HTTP_202_ACCEPTED:
                return valid_json
            # |--------------------------------------------------------------------------------------------------------|

            # dictionary validation |----------------------------------------------------------------------------------|
            response: dict = request.json
            
            if not isinstance(response['filter'], dict):
                return "ONLY JSON FILTER ARE ALLOWED", HTTP_400_BAD_REQUEST
            # |--------------------------------------------------------------------------------------------------------|

            return func(*args, **kwargs)
        
        return wrapper

    @staticmethod
    def update_document(func: Callable[..., Any]) -> Callable[..., Callable[..., tuple[str, int]]]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Callable[..., tuple[str, int]]:
            
            fields: list[str] = ["database", 'collection', '_id', 'update']
            
            # json validation |----------------------------------------------------------------------------------------|
            valid_json = json_fields_validation(fields)
            if valid_json[1] != HTTP_202_ACCEPTED:
                return valid_json
            # |--------------------------------------------------------------------------------------------------------|
            
            # dict validation |----------------------------------------------------------------------------------------|
            valid_dict: dict[str, Any] = dictionary_validation(request.json['update'])
            if valid_dict[1] != HTTP_202_ACCEPTED:
                return valid_dict
            # |--------------------------------------------------------------------------------------------------------|
            
            # fobbiden update fields |---------------------------------------------------------------------------------|
            forbbiden_fields: list[str] = ["datetime", "_id", "user"]
            for i in request.json['update']:
                if i in forbbiden_fields:
                    return f"UPDATING FIELD {i} IS NOT ALLOWED", HTTP_403_FORBIDDEN
            # |--------------------------------------------------------------------------------------------------------|
                        
            return func(*args, **kwargs)
        return wrapper