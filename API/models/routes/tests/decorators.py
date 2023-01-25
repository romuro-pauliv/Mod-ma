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
                
                # + Request +
                request_value: dict[str, Any] = request.json 
                
                # | Json validation |----------------------------------------------------------------------------------|
                validate_fields = Validate.JSON.fields(["database"])
                if validate_fields[1] != HTTP_202_ACCEPTED:
                    return validate_fields
                # |----------------------------------------------------------------------------------------------------|
                
                # | String validation |--------------------------------------------------------------------------------|
                validate_value_str = Validate.STRING.value_must_be_str(request_value['database'])
                if validate_value_str[1] != HTTP_202_ACCEPTED:
                    return validate_value_str
                
                validate_string_type = Validate.STRING.type_(request_value['database'])
                if validate_string_type[1] != HTTP_202_ACCEPTED:
                    return validate_string_type
                
                validate_string_length = Validate.STRING.length(request_value['database'], 4)
                if validate_string_length[1] != HTTP_202_ACCEPTED:
                    return validate_string_length

                validate_string_character = Validate.STRING.character(request_value['database'])
                if validate_string_character[1] != HTTP_202_ACCEPTED:
                    return validate_string_character
                # |----------------------------------------------------------------------------------------------------|
                
                # + return +
                return func(*args, **kwargs)
            return wrapper