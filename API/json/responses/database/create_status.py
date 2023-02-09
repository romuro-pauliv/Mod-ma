# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                      API.json.reponses.database.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from API.status import *
from API.json.tools.tools import response_structure
# |--------------------------------------------------------------------------------------------------------------------|

class Reponses(object):
    class R4XX(object):
        @staticmethod
        def name_not_allowed(database_name: str) -> tuple[dict, int]:
            return response_structure(f"FORBIDDEN - NAME [{database_name}] NOT ALLOWED", HTTP_403_FORBIDDEN)
        
        @ staticmethod
        def name_in_use(database_name: str) -> tuple[dict, int]:
            return response_structure(f"FORBIDDEN - NAME [{database_name}] IN USE", HTTP_403_FORBIDDEN)
    
    class R2XX(object):
        @staticmethod
        def create(database_name: str) -> tuple[dict, str]:
            return response_structure(f"[{database_name}] CREATED", HTTP_201_CREATED)
