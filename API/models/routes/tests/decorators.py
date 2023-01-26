# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                              API.models.routes.tests.decorators.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# imports |------------------------------------------------------------------------------------------------------------|
from API.status import *
from API.models.tools.validations import Validate


from flask import request
from typing import Callable, Any
from functools import wraps
# |--------------------------------------------------------------------------------------------------------------------|

class Model(object):
    class Create(object):
        @staticmethod
        def database(func: Callable[..., Any]) -> Callable[..., Callable[..., tuple[str, int]]]:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Callable[..., tuple[str, int]]:
                # + Fields +
                fields: list[str] = ["database"]
                
                # | Json validation |----------------------------------------------------------------------------------|
                validate_fields = Validate.JSON.fields(fields)
                if validate_fields[1] != HTTP_202_ACCEPTED:
                    return validate_fields
                # |----------------------------------------------------------------------------------------------------|
                
                # + request values +
                values_: list[str] = [request.json[i] for i in fields]
                                
                # | String validation |--------------------------------------------------------------------------------|
                for i in values_:
                    validate_value_str: tuple[str, int] = Validate.STRING.str_type(i)
                    if validate_value_str[1] != HTTP_202_ACCEPTED:
                        return validate_value_str
               
                validate_string_length = Validate.STRING.length(values_, 4)
                if validate_string_length[1] != HTTP_202_ACCEPTED:
                    return validate_string_length

                validate_string_character = Validate.STRING.character(values_)
                if validate_string_character[1] != HTTP_202_ACCEPTED:
                    return validate_string_character
                # |----------------------------------------------------------------------------------------------------|
                
                # + return +
                return func(*args, **kwargs)
            return wrapper
        
        @staticmethod
        def collection(func: Callable[..., Any]) -> Callable[..., Callable[..., tuple[str, int]]]:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Callable[..., tuple[str, int]]:
                # + Fields +
                fields: list[str] = ["database", "collection"]

                # | Json validation |----------------------------------------------------------------------------------|
                validate_json: tuple[str, int] = Validate.JSON.fields(fields)
                if validate_json[1] != HTTP_202_ACCEPTED:
                    return validate_json
                # |----------------------------------------------------------------------------------------------------|
                
                # + request values +
                values_: list[str] = [request.json[i] for i in fields]
                
                # String validation |----------------------------------------------------------------------------------|
                for i in values_:
                    validate_value_str: tuple[str, int] = Validate.STRING.str_type(i)
                    if validate_value_str[1] != HTTP_202_ACCEPTED:
                        return validate_value_str
                
                validate_string_length: tuple[str, int] = Validate.STRING.length(values_, 4)
                print(validate_string_length)
                if validate_string_length[1] != HTTP_202_ACCEPTED:
                    return validate_string_length
                
                validate_string_character: tuple[str, int] = Validate.STRING.character(values_)
                if validate_string_character[1] != HTTP_202_ACCEPTED:
                    return validate_string_character
                # |----------------------------------------------------------------------------------------------------|
                
                # + return +
                return func(*args, **kwargs)
            return wrapper