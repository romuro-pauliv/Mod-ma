# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                         API.models.routes.collection.decorators.py |
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
        def document(func: Callable[..., Any]) -> Callable[..., Callable[..., tuple[Union[str, dict], int]]]:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Callable[..., tuple[Union[str, dict], int]]:
                # + Fields +
                fields: list[str] = ["database", "collection", "document"]
                forbidden_document_fields: list[str] = ["_id", "datetime", "user"]
                
                # | Json validation |----------------------------------------------------------------------------------|
                validate_format: tuple[str, int] = Validate.JSON.format_(request.json)
                if validate_format[1] != HTTP_202_ACCEPTED:
                    return validate_format
                
                validate_json: tuple[str, int] = Validate.JSON.fields(fields)
                if validate_json[1] != HTTP_202_ACCEPTED:
                    return validate_json
                # |----------------------------------------------------------------------------------------------------|
                
                # Json document validation |---------------------------------------------------------------------------|
                document: dict[str, Any] = request.json['document']
                
                validate_document_json_format: list[str, int] = Validate.JSON.format_(document)
                if validate_document_json_format[1] != HTTP_202_ACCEPTED:
                    return validate_document_json_format
                
                validate_forbidden_fields: list[str, int] = Validate.JSON.forbidden_fields(
                    document, forbidden_document_fields)
                if validate_forbidden_fields[1] != HTTP_202_ACCEPTED:
                    return validate_forbidden_fields
                
                document_fields: list[str] = [i for i in document.keys()]
                
                validate_character_fields: list[str, int] = Validate.STRING.character(document_fields)
                if validate_character_fields[1] != HTTP_202_ACCEPTED:
                    return validate_character_fields
                # |----------------------------------------------------------------------------------------------------|
                
                return func(*args, **kwargs)
            return wrapper
    
    class Read(object):
        @staticmethod
        def document(func: Callable[..., Any]) -> Callable[..., Callable[..., tuple[Union[list[dict], str], int]]]:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Callable[..., tuple[Union[list[dict], str], int]]:
                # + Fields +
                fields: list[str] = ["database", "collection", "filter"]
                
                # | Json validation |----------------------------------------------------------------------------------|
                validate_format: tuple[str, int] = Validate.JSON.format_(request.json)
                if validate_format[1] != HTTP_202_ACCEPTED:
                    return validate_format
                                
                validate_json: tuple[str, int] = Validate.JSON.fields(fields)
                if validate_json[1] != HTTP_202_ACCEPTED:
                    return validate_json
                # |----------------------------------------------------------------------------------------------------|
                
                # | Filter validation |--------------------------------------------------------------------------------|
                filter_: dict[str, Any] = request.json["filter"]
                
                validate_filter_json: tuple[str, int] = Validate.JSON.is_json(filter_)
                if validate_filter_json[1] != HTTP_202_ACCEPTED:
                    return validate_filter_json
                
                filter_fields: list[str] = [i for i in filter_.keys()]
                
                validate_character: tuple[str, int] = Validate.STRING.character(filter_fields)
                if validate_character[1] != HTTP_202_ACCEPTED:
                    return validate_character
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
                validate_format: tuple[str, int] = Validate.JSON.format_(request.json, False)
                if validate_format[1] != HTTP_202_ACCEPTED:
                    return validate_format
                
                validate_json: tuple[str, int] = Validate.JSON.fields(fields)
                if validate_json[1] != HTTP_202_ACCEPTED:
                    return validate_json
                # |----------------------------------------------------------------------------------------------------|
                
                # | Update validation |--------------------------------------------------------------------------------|
                validate_update_format: tuple[str, int] = Validate.JSON.format_(request.json['update'])
                if validate_update_format[1] != HTTP_202_ACCEPTED:
                    return validate_update_format
                
                udpate_document: dict[str, Any] = request.json['update']
                
                validate_if_include_data: tuple[dict, int] = Validate.JSON.need_data_in_update_json(udpate_document)
                if validate_if_include_data[1] != HTTP_202_ACCEPTED:
                    return validate_if_include_data
                
                validate_update_forbidden_fields: tuple[str, int] = Validate.JSON.forbidden_fields(
                    request.json['update'], forbidden_update_fields
                )
                if validate_update_forbidden_fields[1] != HTTP_202_ACCEPTED:
                    return validate_update_forbidden_fields
                
                update_document_fields: list[str] = [i for i in udpate_document.keys()]
                
                validate_fields_character: tuple[dict, int] = Validate.STRING.character(update_document_fields)
                if validate_fields_character[1] != HTTP_202_ACCEPTED:
                    return validate_fields_character
                # |----------------------------------------------------------------------------------------------------|
                
                return func(*args, **kwargs)
            return wrapper
    
    class Delete(object):
        @staticmethod
        def document(func: Callable[..., Any]) -> Callable[..., Callable[..., tuple[str, int]]]:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Callable[..., tuple[str, int]]:
                # + Fields +
                fields: list[str] = ["database", "collection", "_id"]
                
                # Json validation |------------------------------------------------------------------------------------|
                validate_format: tuple[dict, int] = Validate.JSON.format_(request.json, False)
                if validate_format[1] != HTTP_202_ACCEPTED:
                    return validate_format
                
                validate_json: tuple[str, int] = Validate.JSON.fields(fields)
                if validate_json[1] != HTTP_202_ACCEPTED:
                    return validate_json
                # |----------------------------------------------------------------------------------------------------|
                
                return func(*args, **kwargs)
            return wrapper