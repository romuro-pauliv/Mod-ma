# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                       API.json.reponses.validation.json_request.py |
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
        def key_error(field: str) -> tuple[dict, int]:
            return response_structure(f"KEY ERROR - NEED [{field}] FIELD", HTTP_400_BAD_REQUEST)
        
        @staticmethod
        def format_error() -> tuple[dict, int]:
            return response_structure("ONLY JSON ARE ALLOWED", HTTP_400_BAD_REQUEST)
        
        @staticmethod
        def characters_amount_model_error(field: str) -> tuple[dict, int]:
            return response_structure(f"THE INFORMED FIELD [{field}] MUST BE MORE THAN 4 CHARACTERS",
                                      HTTP_400_BAD_REQUEST)
        
        @staticmethod
        def internal_json_format_error() -> tuple[dict, int]:
            return response_structure("ONLY JSON FILTER ARE ALLOWED", HTTP_400_BAD_REQUEST)
        
        @staticmethod
        def forbidden_fields_error(field: str) -> tuple[dict, int]:
            return response_structure(f"UPDATING FIELD [{field}] IS NOT ALLOWED", HTTP_403_FORBIDDEN)
        
        @staticmethod
        def need_data_in_json() -> tuple[dict, int]:
            return response_structure("NEED DATA IN UPDATE DOCUMENT", HTTP_400_BAD_REQUEST)
        
    class R2XX(object):
        @staticmethod
        def valid_field() -> tuple[str, int]:
            return "VALID FIELD", HTTP_202_ACCEPTED