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
        @staticmethod
        def database_not_found(database_name: str) -> tuple[dict[str], int]:
            return response_structure(f"DATABASE [{database_name}] NOT FOUND", HTTP_404_NOT_FOUND)
        
        @staticmethod
        def collection_name_in_use(collection_name: str) -> tuple[dict[str], int]:
            return response_structure(f"COLLECTION NAME [{collection_name}] IN USE", HTTP_403_FORBIDDEN)
        
    class R2XX(object):
        @staticmethod
        def collection_created(collection_name: str) -> tuple[dict[str], int]:
            return response_structure(f"[{collection_name}] COLLECTION CREATED", HTTP_201_CREATED)
