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
            return response_structure("COLON ERROR - BAD REQUEST", HTTP_400_BAD_REQUEST)
        
        def colon_not_allowed() -> tuple[dict[str], int]:
            return response_structure("CHARACTER [:] NOT ALLOWED - BAD REQUEST", HTTP_400_BAD_REQUEST)
        
        def no_colon_identify() -> tuple[dict[str], int]:
            return response_structure("NO COLON IDENTIFY - BAD REQUEST", HTTP_400_BAD_REQUEST)
        
        def no_data() -> tuple[dict[str], int]:
            return response_structure("NO HEADER DATA - BAD REQUEST", HTTP_400_BAD_REQUEST)
        
        def binascii_error() -> tuple[dict[str], int]:
            return response_structure("BINASCII ERROR - BAD REQUEST", HTTP_400_BAD_REQUEST)
        