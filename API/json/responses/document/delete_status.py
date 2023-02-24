# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                      API.json.reponses.document.py |
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

        @staticmethod
        def document_not_found(document_id: str) -> tuple[dict[str], int]:
            return response_structure(f"DOCUMENT WITH ID [{document_id}] NOT FOUND", HTTP_404_NOT_FOUND)
    
    class R2XX(object):
        @staticmethod
        def document_deleted(_id: str) -> tuple[dict[str], int]:
            return response_structure(f"DOCUMENT WITH ID [{_id}] DELETED", HTTP_202_ACCEPTED)