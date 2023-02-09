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

class Responses(object):
    class R4XX(object):
        @staticmethod
        def not_found(database_name: str) -> tuple[dict[str], int]:
            return response_structure(f"DATABASE [{database_name}] NOT FOUND", HTTP_404_NOT_FOUND)
        
    class R2XX(object):
        @staticmethod
        def delete_database(database_name: str) -> tuple[dict[str], int]:
            return response_structure(f"[{database_name}] DATABASE DELETED", HTTP_202_ACCEPTED)