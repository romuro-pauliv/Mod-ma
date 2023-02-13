# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                    API.models.tools.validations.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# imports |------------------------------------------------------------------------------------------------------------|
from API.status import *
from API.json.responses.validation import json_status, string_status

from flask import request
from typing import Any, Union
# |--------------------------------------------------------------------------------------------------------------------|


class Validate(object):
    # | JSON |=========================================================================================================|
    class JSON(object):
        @staticmethod
        def fields(required_fields: list[str]) -> tuple[str, int]:
            for fld in required_fields:
                try:
                    if request.json[fld]:
                        pass
                except KeyError:
                    return json_status.Responses.R4XX.key_error(fld)
            return json_status.Responses.R2XX.valid_field()
        
        @staticmethod
        def format_(archive: dict[str, Any]) -> tuple[str, int]:
            # + Type verification +
            if not isinstance(archive, dict):
                return json_status.Responses.R4XX.format_error()
            
            # + fields +
            for key in archive.keys():
                if len(key) < 4:
                    return json_status.Responses.R4XX.characters_amount_model_error(key)
            return json_status.Responses.R2XX.valid_field()
        
        @staticmethod
        def is_json(archive: dict[str, Any]) -> tuple[str, int]:
            if not isinstance(archive, dict):
                return json_status.Responses.R4XX.internal_json_format_error()
            return json_status.Responses.R2XX.valid_field()
        
        @staticmethod
        def forbidden_fields(archive: dict[str, Any], forbidden_fields: list[str]) -> tuple[str, int]:
            for field in archive:
                if field in forbidden_fields:
                    return json_status.Responses.R4XX.forbidden_fields_error(field)
            return json_status.Responses.R2XX.valid_field()
    # |================================================================================================================|
    
    # | STRING |=======================================================================================================|
    class STRING(object):
        @staticmethod
        def str_type(value: str) -> tuple[str, int]:
            if not isinstance(value, str):
                return string_status.Responses.R4XX.only_string_error()
            return string_status.Responses.R2XX.valid_string_type()
        
        @staticmethod
        def length(string: Union[str, list[str]], length_: int) -> tuple[str, int]:
            if isinstance(string, list):
                for strg in string:
                    if len(strg) < length_:
                        return string_status.Responses.R4XX.length_error(strg, length_)
                return string_status.Responses.R2XX.valid_length()
            elif len(string) < length_:
                return string_status.Responses.R4XX.length_error(string, length_)
            return string_status.Responses.R2XX.valid_length()
        
        @staticmethod
        def character(string: Union[str, list[str]]) -> tuple[str, int]:
            if isinstance(string, list):
                for strg in string:
                    for _char in strg:
                        if _char in "!\"#$%&'()*+,./:;<=>?@[\]^`{|}~ \t\n\r\x0b\x0c":
                            return string_status.Responses.R4XX.character_error(strg, _char)
                return string_status.Responses.R2XX.valid_character()
            else:
                for _char in string:
                    if _char in "!\"#$%&'()*+,./:;<=>?@[\]^`{|}~ \t\n\r\x0b\x0c":
                        return string_status.Responses.R4XX.character_error(string, _char)
                return string_status.Responses.R2XX.valid_character()
        