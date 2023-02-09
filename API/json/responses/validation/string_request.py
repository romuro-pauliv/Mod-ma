# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                     API.json.reponses.validation.string_request.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from API.status import *
from API.json.tools.tools import response_structure
# |--------------------------------------------------------------------------------------------------------------------|


class Responses(object):
    class R4XX(object):
        @staticmethod
        def only_string_error() -> tuple[dict, int]:
            return response_structure("ONLY STRING ARE ALLOWED", HTTP_400_BAD_REQUEST)
    
        @staticmethod
        def length_error(value_name: str, length: int) -> tuple[dict, int]:
            return response_structure(
                f"THE INFORMED NAME [{value_name}] MUST BE MORE THAN [{length}] CHARACTERS", HTTP_400_BAD_REQUEST
            )
        
        @staticmethod
        def character_error(value_name: str, character_not_allowed: str) -> tuple[dict, int]:
            return response_structure(
                f"CHARACTER [{character_not_allowed}] IN [{value_name}] NOT ALLOWED", HTTP_400_BAD_REQUEST
            )
        
    class R2XX(object):
        @staticmethod
        def valid_string_type() -> tuple[str, int]:
            return "VALID TYPE", HTTP_202_ACCEPTED
        
        @staticmethod
        def valid_length() -> tuple[str, int]:
            return "VALID LENGTH", HTTP_202_ACCEPTED

        @staticmethod
        def valid_character() -> tuple[str, int]:
            return "VALID CHARACTER", HTTP_202_ACCEPTED