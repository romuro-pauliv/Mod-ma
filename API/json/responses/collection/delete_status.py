# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                        API.json.reponses.collection.read_status.py |
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
        def database_not_found(database_name: str) -> tuple[dict[str], int]:
            return response_structure(f"DATABASE [{database_name}] NOT FOUND", HTTP_404_NOT_FOUND)
        
        @staticmethod
        def collection_not_found(collection_name: str) -> tuple[dict[str], int]:
            return response_structure(f"COLLECTION [{collection_name}] NOT FOUND", HTTP_404_NOT_FOUND)
    
    class R2XX(object):
        @staticmethod
        def collection_deleted(collection_name: str) -> tuple[dict[str], int]:
            return response_structure(f"[{collection_name}] COLLECTION DELETED", HTTP_202_ACCEPTED)