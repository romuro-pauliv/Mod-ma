# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                     API.json.reponses.ipt_token.py |
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
        def colon_error() -> tuple[dict, int]:
            return response_structure("WAS NOT IDENTIFIED [:] COLON IN THE CREDENTIALS", HTTP_400_BAD_REQUEST)
        
        @staticmethod
        def data_error() -> tuple[dict, int]:
            return response_structure("A STRING WAS NOT IDENTIFIED IN THE TOKEN", HTTP_400_BAD_REQUEST)
        
        @staticmethod
        def invalid_token() -> tuple[dict, int]:
            return response_structure("INVALID TOKEN", HTTP_403_FORBIDDEN)
        
        @staticmethod
        def expired_token() -> tuple[dict, int]:
            return response_structure("EXPIRED TOKEN", HTTP_403_FORBIDDEN)
        
        @staticmethod
        def ip_error() -> tuple[dict, int]:
            return response_structure("IP ADDRESS DOES NOT MATCH", HTTP_403_FORBIDDEN)
    
    class R2XX(object):
        @staticmethod
        def valid_token() -> tuple[str, int]:
            return "VALID TOKEN", HTTP_200_OK