# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                      API.json.reponses.collection.create_status.py |
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
        def colon_error() -> tuple[dict[str], int]:
            return response_structure("CHARACTER [:] NOT ALLOWED", HTTP_400_BAD_REQUEST)
        
        def binascii_error() -> tuple[dict[str], int]:
            return response_structure("BINASCII ERROR - BAD REQUEST", HTTP_400_BAD_REQUEST)
        
        def invalid_argument() -> tuple[dict[str], int]:
            return response_structure("INVALID ARGUMENT INFORMED - BAD REQUEST", HTTP_400_BAD_REQUEST)
        
        def invalid_header_data() -> tuple[dict[str], int]:
            return response_structure("INVALID HEADER DATA - BAD REQUEST", HTTP_400_BAD_REQUEST)
    
    class R2XX(object):
        def valid(decrypt_credentials: list[str]) -> tuple[list[str], int]:
            return decrypt_credentials, HTTP_200_OK