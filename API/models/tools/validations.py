# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                    API.models.tools.validations.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# imports |------------------------------------------------------------------------------------------------------------|
from API.status import *

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
                    return "BAD REQUEST - KEY ERROR", HTTP_400_BAD_REQUEST
            return "VALID FIELD", HTTP_202_ACCEPTED
        
        @staticmethod
        def format_(archive: dict[str, Any]) -> tuple[str, int]:
            # + Type verification +
            if not isinstance(archive, dict):
                return "ONLY JSON ARE ALLOWED", HTTP_400_BAD_REQUEST
            
            # + fields +
            for key in archive.keys():
                if len(key) < 4:
                    return "THE INFORMED FIELD MUST BE MORE THAN 4 CHARACTERS", HTTP_400_BAD_REQUEST
            
            return "VALID JSON", HTTP_202_ACCEPTED
        
        @staticmethod
        def is_json(archive: dict[str, Any]) -> tuple[str, int]:
            if not isinstance(archive, dict):
                return "ONLY JSON FILTER ARE ALLOWED", HTTP_400_BAD_REQUEST
            return "VALID JSON", HTTP_202_ACCEPTED
        
        @staticmethod
        def forbidden_fields(archive: dict[str, Any], forbidden_fields: list[str]) -> tuple[str, int]:
            for field in archive:
                if field in forbidden_fields:
                    return f"UPDATING FIELD [{field.upper()}] IS NOT ALLOWED", HTTP_403_FORBIDDEN
            return "VALID FIELDS", HTTP_202_ACCEPTED
    # |================================================================================================================|
    
    # | STRING |=======================================================================================================|
    class STRING(object):
        @staticmethod
        def str_type(value: str) -> tuple[str, int]:
            if not isinstance(value, str):
                return "ONLY STRING ARE ALLOWED", HTTP_400_BAD_REQUEST
            return "VALID TYPE", HTTP_202_ACCEPTED
        
        @staticmethod
        def length(string: Union[str, list[str]], length_: int) -> tuple[str, int]:
            if isinstance(string, list):
                for strg in string:
                    if len(strg) < length_:
                        return f"THE INFORMED NAME MUST BE MORE THAN {length_} CHARACTERS", HTTP_400_BAD_REQUEST
                return "VALID LENGTH", HTTP_202_ACCEPTED
            elif len(string) < length_:
                return f"THE INFORMED NAME MUST BE MORE THAN {length_} CHARACTERS", HTTP_400_BAD_REQUEST
            return "VALID LENGTH", HTTP_202_ACCEPTED
        
        @staticmethod
        def character(string: Union[str, list[str]]) -> tuple[str, int]:
            if isinstance(string, list):
                for strg in string:
                    for _char in strg:
                        if _char in "!\"#$%&'()*+,./:;<=>?@[\]^`{|}~ \t\n\r\x0b\x0c":
                            return f"CHARACTER [{str(_char)}] NOT ALLOWED", HTTP_400_BAD_REQUEST
                return "VALID CHARACTER", HTTP_202_ACCEPTED
            else:
                for _char in string:
                    if _char in "!\"#$%&'()*+,./:;<=>?@[\]^`{|}~ \t\n\r\x0b\x0c":
                        return f"CHARACTER [{str(_char)}] NOT ALLOWED", HTTP_400_BAD_REQUEST
                return "VALID CHARACTER", HTTP_202_ACCEPTED
        