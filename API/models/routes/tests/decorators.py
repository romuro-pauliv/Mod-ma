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
from typing import Callable, Any, Union
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

                validate_format: tuple[str, int] = Validate.JSON.format_(request.json)
                if validate_format[1] != HTTP_202_ACCEPTED:
                    return validate_format
                # |----------------------------------------------------------------------------------------------------|
                
                # + request values +
                values_: list[str] = [request.json[i] for i in fields]
                                
                # | String validation |--------------------------------------------------------------------------------|
                for i in values_:
                    validate_value_str: tuple[str, int] = Validate.STRING.str_type(i)
                    if validate_value_str[1] != HTTP_202_ACCEPTED:
                        return validate_value_str
               
                validate_string_length: tuple[str, int] = Validate.STRING.length(values_, 4)
                if validate_string_length[1] != HTTP_202_ACCEPTED:
                    return validate_string_length

                validate_string_character: tuple[str, int] = Validate.STRING.character(values_)
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
                
                validate_format: tuple[str, int] = Validate.JSON.format_(request.json)
                if validate_format[1] != HTTP_202_ACCEPTED:
                    return validate_format
                # |----------------------------------------------------------------------------------------------------|
                
                # + request values +
                values_: list[str] = [request.json[i] for i in fields]
                
                # String validation |----------------------------------------------------------------------------------|
                for i in values_:
                    validate_value_str: tuple[str, int] = Validate.STRING.str_type(i)
                    if validate_value_str[1] != HTTP_202_ACCEPTED:
                        return validate_value_str
                
                validate_string_length: tuple[str, int] = Validate.STRING.length(values_, 4)
                if validate_string_length[1] != HTTP_202_ACCEPTED:
                    return validate_string_length
                
                validate_string_character: tuple[str, int] = Validate.STRING.character(values_)
                if validate_string_character[1] != HTTP_202_ACCEPTED:
                    return validate_string_character
                # |----------------------------------------------------------------------------------------------------|
                
                # + return +
                return func(*args, **kwargs)
            return wrapper
        
        @staticmethod
        def document(func: Callable[..., Any]) -> Callable[..., Callable[..., tuple[Union[str, dict], int]]]:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Callable[..., tuple[Union[str, dict], int]]:
                # + Fields +
                fields: list[str] = ["database", "collection", "document"]
                forbidden_document_fields: list[str] = ["_id", "datetime", "user"]
                
                # | Json validation |----------------------------------------------------------------------------------|
                validate_json: tuple[str, int] = Validate.JSON.fields(fields)
                if validate_json[1] != HTTP_202_ACCEPTED:
                    return validate_json
                
                validate_format: tuple[str, int] = Validate.JSON.format_(request.json)
                if validate_format[1] != HTTP_202_ACCEPTED:
                    return validate_format
                # |----------------------------------------------------------------------------------------------------|
                
                # + request values +
                values_: list[str] = [request.json[i] for i in fields]
                
                # | String validation |--------------------------------------------------------------------------------|
                for i in values_[0:1]:
                    validate_value_str: tuple[str, int] = Validate.STRING.str_type(i)
                    if validate_value_str[1] != HTTP_202_ACCEPTED:
                        return validate_value_str
                
                validate_string_length: tuple[str, int] = Validate.STRING.length(values_[0:1], 4)
                if validate_string_length[1] != HTTP_202_ACCEPTED:
                    return validate_string_length
                
                validate_string_character: tuple[str, int] = Validate.STRING.character(values_[0:1])
                if validate_string_character[1] != HTTP_202_ACCEPTED:
                    return validate_string_character
                # |----------------------------------------------------------------------------------------------------|
                
                # Json document validation |---------------------------------------------------------------------------|
                validate_document_json_format: list[str, int] = Validate.JSON.format_(request.json['document'])
                if validate_document_json_format[1] != HTTP_202_ACCEPTED:
                    return validate_document_json_format
                
                validate_forbidden_fields: list[str, int] = Validate.JSON.forbidden_fields(
                    request.json['document'], forbidden_document_fields)
                if validate_forbidden_fields[1] != HTTP_202_ACCEPTED:
                    return validate_forbidden_fields
                # |----------------------------------------------------------------------------------------------------|
                
                return func(*args, **kwargs)
            return wrapper
    
    class Read(object):
        @staticmethod
        def collection(func: Callable[..., Any]) -> Callable[..., Callable[..., tuple[Union[list[str], str], int]]]:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Callable[..., tuple[Union[list[str], str], int]]:
                # + Fields +
                fields: list[str] = ["database"]
                
                # | Json validation |----------------------------------------------------------------------------------|
                validate_json: tuple[str, int] = Validate.JSON.fields(fields)
                if validate_json[1] != HTTP_202_ACCEPTED:
                    return validate_json
                # |----------------------------------------------------------------------------------------------------|
                
                return func(*args, **kwargs)
            return wrapper

        @staticmethod
        def document(func: Callable[..., Any]) -> Callable[..., Callable[..., tuple[Union[list[dict], str], int]]]:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Callable[..., tuple[Union[list[dict], str], int]]:
                # + Fields +
                fields: list[str] = ["database", "collection", "filter"]
                
                # | Json validation |----------------------------------------------------------------------------------|
                validate_json: tuple[str, int] = Validate.JSON.fields(fields)
                if validate_json[1] != HTTP_202_ACCEPTED:
                    return validate_json
                # |----------------------------------------------------------------------------------------------------|
                
                # | Filter validation |--------------------------------------------------------------------------------|
                validate_filter_json: tuple[str, int] = Validate.JSON.is_json(request.json['filter'])
                if validate_filter_json[1] != HTTP_202_ACCEPTED:
                    return validate_filter_json
                # |----------------------------------------------------------------------------------------------------|
                
                return func(*args, **kwargs)
            return wrapper
    
    class Update(object):
        @staticmethod
        def document(func: Callable[..., Any]) -> Callable[..., Callable[..., tuple[str, int]]]:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Callable[..., tuple[str, int]]:
                # + Fields +
                fields: list[str] = ["database", "collection", "_id", "update"]
                forbidden_update_fields: list[str] = ["datetime", "_id", "user"]
                
                # | Json validation |----------------------------------------------------------------------------------|
                validate_json: tuple[str, int] = Validate.JSON.fields(fields)
                if validate_json[1] != HTTP_202_ACCEPTED:
                    return validate_json
                # |----------------------------------------------------------------------------------------------------|
                
                # | Update validation |--------------------------------------------------------------------------------|
                validate_update_format: tuple[str, int] = Validate.JSON.format_(request.json['update'])
                if validate_update_format[1] != HTTP_202_ACCEPTED:
                    return validate_update_format
                
                validate_update_forbidden_fields: tuple[str, int] = Validate.JSON.forbidden_fields(
                    request.json['update'], forbidden_update_fields
                )
                if validate_update_forbidden_fields[1] != HTTP_202_ACCEPTED:
                    return validate_update_forbidden_fields
                # |----------------------------------------------------------------------------------------------------|
                
                return func(*args, **kwargs)
            return wrapper
        
    class Delete(object):
        @staticmethod
        def database(func: Callable[..., Any]) -> Callable[..., Callable[..., tuple[str, int]]]:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Callable[..., tuple[str, int]]:
                # + Fields +
                fields: list[str] = ["database"]
                
                # Json validation |------------------------------------------------------------------------------------|
                validate_json: tuple[str, int] = Validate.JSON.fields(fields)
                if validate_json[1] != HTTP_202_ACCEPTED:
                    return validate_json

                validate_format: tuple[str, int] = Validate.JSON.format_(request.json)
                if validate_format[1] != HTTP_202_ACCEPTED:
                    return validate_format
                # |----------------------------------------------------------------------------------------------------|
                
                # + Request values +
                values_: list[str] = [request.json[i] for i in fields]
                
                # | String validation |--------------------------------------------------------------------------------|
                for i in values_:
                    validate_value_str: tuple[str, int] = Validate.STRING.str_type(i)
                    if validate_value_str[1] != HTTP_202_ACCEPTED:
                        return validate_value_str
                # |----------------------------------------------------------------------------------------------------|
                
                return func(*args, **kwargs)
            return wrapper
        
        @staticmethod
        def collection(func: Callable[..., Any]) -> Callable[..., Callable[..., tuple[str, int]]]:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Callable[..., tuple[str, int]]:
                # + Fields +
                fields: list[str] = ["database", "collection"]
                
                # Json validation |------------------------------------------------------------------------------------|
                validate_json: tuple[str, int] = Validate.JSON.fields(fields)
                if validate_json[1] != HTTP_202_ACCEPTED:
                    return validate_json
                
                validate_format: tuple[str, int] = Validate.JSON.format_(request.json)
                if validate_format[1] != HTTP_202_ACCEPTED:
                    return validate_format
                # |----------------------------------------------------------------------------------------------------|

                # + Request values +
                values_: list[str] = [request.json[i] for i in fields]
                
                # | String validation |--------------------------------------------------------------------------------|
                for i in values_:
                    validate_value_str: tuple[str, int] = Validate.STRING.str_type(i)
                    if validate_value_str[1] != HTTP_202_ACCEPTED:
                        return validate_value_str
                # |----------------------------------------------------------------------------------------------------|
                
                return func(*args, **kwargs)
            return wrapper
        
        @staticmethod
        def document(func: Callable[..., Any]) -> Callable[..., Callable[..., tuple[str, int]]]:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Callable[..., tuple[str, int]]:
                # + Fields +
                fields: list[str] = ["database", "collection", "doc_id"]
                
                # Json validation |------------------------------------------------------------------------------------|
                validate_json: tuple[str, int] = Validate.JSON.fields(fields)
                if validate_json[1] != HTTP_202_ACCEPTED:
                    return validate_json
                
                validate_format: tuple[str, int] = Validate.JSON.format_(request.json)
                if validate_format[1] != HTTP_202_ACCEPTED:
                    return validate_format
                # |----------------------------------------------------------------------------------------------------|
                
                # + Request values +
                values_: list[str] = [request.json[i] for i in fields]
                
                # | String validation |--------------------------------------------------------------------------------|
                for i in values_:
                    validate_value_str: tuple[str, int] = Validate.STRING.str_type(i)
                    if validate_value_str[1] != HTTP_202_ACCEPTED:
                        return validate_value_str
                # |----------------------------------------------------------------------------------------------------|
                
                return func(*args, **kwargs)
            return wrapper